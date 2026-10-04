#!/usr/bin/env python3
"""Read complete JSONL events while a worker may still be writing the file."""
import argparse
import json
import math
import os
from pathlib import Path
import signal
import subprocess
import time
import re
import sys


def read_events(path):
    with open(path, encoding="utf-8", errors="replace") as source:
        for line in source:
            try:
                event = json.loads(line)
            except ValueError:
                continue
            if isinstance(event, dict):
                yield event


def object_of(value):
    return value if isinstance(value, dict) else {}


def list_of(value):
    return value if isinstance(value, list) else []


def numeric(value):
    return value if isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) else 0


def compact(value, limit=200):
    if not isinstance(value, str):
        value = json.dumps(value, ensure_ascii=False)
    return " ".join(value.split())[:limit]


def claude_windows(event):
    info = object_of(event.get("rate_limit_info"))
    windows = object_of(info.get("unifiedWindows"))
    return {key: value for key, value in windows.items() if isinstance(value, dict)}


def codex_item(event):
    kind = event.get("type")
    if kind in ("error", "turn.failed"):
        return "[result] " + compact(event)
    if kind != "item.completed":
        return None
    item = object_of(event.get("item"))
    kind = item.get("type")
    if kind == "agent_message":
        return "[msg] " + compact(item.get("text", ""))
    if kind == "command_execution":
        return "[cmd] " + compact(f"{compact(item.get('command', ''), 160)} -> exit {item.get('exit_code')}")
    if kind == "file_change":
        changes = list_of(item.get("changes"))
        return "[file] " + compact(", ".join(f"{c.get('kind', '')}:{c.get('path', '')}" for c in changes if isinstance(c, dict)))
    if kind == "reasoning":
        return "[think] " + compact(item.get("text", ""), 160)
    if kind == "todo_list":
        tasks = list_of(item.get("items"))
        return "[todo] " + compact(" | ".join(("x" if i.get("completed") else " ") + " " + str(i.get("text", "")) for i in tasks if isinstance(i, dict)))
    return "[tool] " + compact(item, 160)


def claude_items(event):
    kind = event.get("type")
    if kind == "result":
        yield "[done] " + ("error " if event.get("is_error") else "") + compact(event.get("result", ""))
    elif kind in ("assistant", "user"):
        content = object_of(event.get("message")).get("content") or []
        if not isinstance(content, list):
            return
        for block in content:
            if not isinstance(block, dict):
                continue
            kind = block.get("type")
            if kind == "thinking":
                yield "[think] " + compact(block.get("thinking", ""), 160)
            elif kind == "text":
                yield "[msg] " + compact(block.get("text", ""))
            elif kind == "tool_use":
                args = object_of(block.get("input"))
                name = block.get("name", "?")
                if name in ("Edit", "Write", "NotebookEdit"):
                    yield "[file] " + compact(f"{name} {args.get('file_path', args.get('notebook_path', ''))}")
                elif name in ("TodoWrite", "TaskCreate", "TaskUpdate"):
                    yield "[todo] " + compact(args)
                elif name == "Bash":
                    yield "[cmd] " + compact(args.get("command", ""), 160)
                else:
                    yield "[tool] " + compact(f"{name} {json.dumps(args, ensure_ascii=False)}")
            elif kind == "tool_result":
                yield "[result] " + ("error " if block.get("is_error") else "") + compact(block.get("content", ""))


def summarize(agent, events):
    meta = dict(THREAD="", TOKENS_IN=0, TOKENS_CACHED=0, TOKENS_OUT=0, TOKENS_REASONING=0)
    if agent == "claude":
        meta["COST_USD"] = 0
    items, final = [], ""
    for event in events:
        kind = event.get("type")
        if agent == "codex":
            if kind == "thread.started":
                meta["THREAD"] = event.get("thread_id", "")
            if kind == "turn.completed":
                usage = object_of(event.get("usage"))
                for field, key in (("TOKENS_IN", "input_tokens"), ("TOKENS_CACHED", "cached_input_tokens"), ("TOKENS_OUT", "output_tokens"), ("TOKENS_REASONING", "reasoning_output_tokens")):
                    meta[field] += numeric(usage.get(key))
            item = object_of(event.get("item"))
            if kind == "item.completed" and item.get("type") == "agent_message":
                final = item.get("text", "")
            line = codex_item(event)
            if line is not None:
                items.append(" ".join(line.split()))
        else:
            if event.get("session_id"):
                meta["THREAD"] = event["session_id"]
            if kind == "result":
                final = event.get("result", "")
                usage = object_of(event.get("usage"))
                # Total input includes both cache reads and cache creation, as in Codex.
                meta["TOKENS_IN"] += sum(numeric(usage.get(k)) for k in ("input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"))
                meta["TOKENS_CACHED"] += numeric(usage.get("cache_read_input_tokens"))
                meta["TOKENS_OUT"] += numeric(usage.get("output_tokens"))
                meta["TOKENS_REASONING"] += numeric(object_of(usage.get("output_tokens_details")).get("thinking_tokens"))
                meta["COST_USD"] += numeric(event.get("total_cost_usd"))
            if kind == "rate_limit_event":
                for window, values in claude_windows(event).items():
                    key = re.sub(r"[^A-Z0-9_]", "_", window.upper())
                    if isinstance(values.get("utilization"), (int, float)):
                        meta["CLAUDE_UTIL_" + key] = values["utilization"]
                    if isinstance(values.get("resetsAt"), (int, float)):
                        meta["CLAUDE_RESETS_" + key] = values["resetsAt"]
            lines = list(claude_items(event))
            if lines:
                items.append(" ".join(" | ".join(lines).split()))
    return meta, items, final


def rollout_usage(thread):
    if not thread:
        return None
    files = list((Path.home() / ".codex/sessions").glob("????/??/??/rollout-*.jsonl"))
    files.sort(key=lambda p: thread not in p.name)
    for path in files:
        matched, usage = thread in path.name, None
        try:
            for event in read_events(path):
                payload = object_of(event.get("payload"))
                if event.get("type") == "session_meta" and payload.get("id") == thread:
                    matched = True
                info = object_of(payload.get("info"))
                counts = info.get("last_token_usage") or info.get("total_token_usage")
                if isinstance(counts, dict):
                    usage = counts
        except OSError:
            continue
        if matched and usage:
            return usage
    return None


def run_worker(cwd, command):
    # Own a process group so cancelling a wrapper also stops its worker's children.
    if sys.platform.startswith("linux"):
        import ctypes
        ctypes.CDLL(None).prctl(36, 1, 0, 0, 0)  # PR_SET_CHILD_SUBREAPER
    interrupted = 0
    deadline = None
    child = None

    def forward(signum, _frame):
        nonlocal interrupted, deadline
        if not interrupted:
            interrupted = signum
            deadline = time.monotonic() + 2
        if child is not None:
            try:
                os.killpg(child.pid, signum)
            except ProcessLookupError:
                pass

    for signum in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
        signal.signal(signum, forward)
    try:
        child = subprocess.Popen(command, cwd=cwd, start_new_session=True,
                                 env=dict(os.environ, AGENT_ROLE="worker"))
    except OSError as error:
        print(f"worker: {error}", file=sys.stderr)
        return 127
    if interrupted:
        forward(interrupted, None)
    while True:
        try:
            rc = child.wait(timeout=.1)
            break
        except subprocess.TimeoutExpired:
            if deadline is not None and time.monotonic() >= deadline:
                try:
                    os.killpg(child.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
    # Reap adopted descendants, escalating if a worker left processes behind.
    try:
        os.killpg(child.pid, signal.SIGTERM)
    except ProcessLookupError:
        pass
    def stop_adopted(signum):
        if not sys.platform.startswith("linux"):
            return
        children = Path(f"/proc/self/task/{os.getpid()}/children")
        try:
            pids = children.read_text().split()
        except OSError:
            return
        for pid in pids:
            try:
                os.kill(int(pid), signum)
            except ProcessLookupError:
                pass

    stop_adopted(signal.SIGTERM)
    deadline = time.monotonic() + 2
    while True:
        try:
            pid, _ = os.waitpid(-1, os.WNOHANG)
        except ChildProcessError:
            break
        if pid:
            continue
        if time.monotonic() >= deadline:
            stop_adopted(signal.SIGKILL)
            try:
                os.killpg(child.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        time.sleep(.01)
    return 128 + interrupted if interrupted else (128 - rc if rc < 0 else rc)


def main():
    if len(sys.argv) > 2 and sys.argv[1] == "worker":
        raise SystemExit(run_worker(sys.argv[2], sys.argv[3:]))
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("meta", "items", "last", "final"))
    parser.add_argument("agent", choices=("codex", "claude"))
    parser.add_argument("file")
    parser.add_argument("n", nargs="?", type=int, default=20)
    args = parser.parse_args()
    try:
        events = list(read_events(args.file))
    except OSError as error:
        print(f"agent_events: cannot read {args.file}: {error.strerror}", file=sys.stderr)
        events = []
    meta, items, final = summarize(args.agent, events)
    if args.command == "meta":
        token_keys = ("TOKENS_IN", "TOKENS_CACHED", "TOKENS_OUT", "TOKENS_REASONING")
        if args.agent == "codex" and not any(meta[key] for key in token_keys):
            usage = rollout_usage(meta["THREAD"])
            fields = ("input_tokens", "cached_input_tokens", "output_tokens", "reasoning_output_tokens")
            for key, field in zip(token_keys, fields):
                meta[key] = numeric(usage.get(field)) if usage else "unknown"
        for key, value in meta.items():
            print(f"{key}={compact(value, 10000)}")
    elif args.command == "items":
        print("\n".join(items[-args.n:] if args.n > 0 else []), end="\n" if items and args.n > 0 else "")
    elif args.command == "last":
        print(f"events={len(items)} last={items[-1] if items else '(none yet)'}")
    elif final:
        print(final)


if __name__ == "__main__":
    main()
