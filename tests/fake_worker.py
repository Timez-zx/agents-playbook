#!/usr/bin/env python3
"""Offline worker: record the call, then replay a captured event stream."""
import json
import os
from pathlib import Path
import sys
import subprocess
import time

agent = Path(sys.argv[0]).name
if agent not in ("codex", "claude"):
    raise SystemExit("Invoke this fake through a codex or claude symlink")
record = Path(os.environ["FAKE_RECORD_DIR"])
record.mkdir(parents=True, exist_ok=True)
args = sys.argv[1:]
if agent == "claude":
    def flag(name):
        return args[args.index(name) + 1]
    mode = flag("--permission-mode")
    assert mode in ("default", "acceptEdits", "bypassPermissions")
    assert flag("--disallowedTools") == ("Task,Agent,Edit,Write,NotebookEdit" if mode == "default" else "Task,Agent")
    if mode == "bypassPermissions":
        assert "--settings" not in args
    else:
        assert flag("--setting-sources") == "" and flag("--permission-prompts") == "none"
        assert "--strict-mcp-config" in args and json.loads(flag("--mcp-config")) == {"mcpServers": {}}
        sandbox = {"enabled": False} if mode == "default" else {"enabled": True, "autoAllowBashIfSandboxed": True, "failIfUnavailable": True, "allowUnsandboxedCommands": False}
        assert json.loads(flag("--settings")) == {"sandbox": sandbox}
    assert "--allowedTools" not in args and "--dangerously-skip-permissions" not in args
(record / f"{agent}.argv.json").write_text(json.dumps(args))
(record / f"{agent}.stdin.txt").write_text(sys.stdin.read())
(record / f"{agent}.env.json").write_text(json.dumps(dict(AGENT_ROLE=os.environ.get("AGENT_ROLE"), CWD=os.getcwd())))
fixture = Path(os.environ["FIXTURES_DIR"]) / ("codex-events.jsonl" if agent == "codex" else "claude-stream.jsonl")
events = fixture.read_text()
if agent == "codex" and "-o" in args:
    final = ""
    for line in events.splitlines():
        event = json.loads(line)
        item = event.get("item", {})
        if event.get("type") == "item.completed" and item.get("type") == "agent_message":
            final = item.get("text", "")
    Path(args[args.index("-o") + 1]).write_text(final + "\n")
if os.environ.get("FAKE_ZERO_USAGE") and agent == "codex":
    lines = [json.loads(line) for line in events.splitlines()]
    for event in lines:
        if event.get("type") == "turn.completed":
            event["usage"] = dict.fromkeys(event["usage"], 0)
    events = "\n".join(json.dumps(event) for event in lines) + "\n"
sys.stdout.write(events)
sys.stdout.flush()
processes = dict(worker=os.getpid())
if os.environ.get("FAKE_DESCENDANT"):
    child = subprocess.Popen([sys.executable, "-c", "import signal,time; signal.signal(signal.SIGTERM,signal.SIG_IGN); time.sleep(60)"], start_new_session=True)
    processes["child"] = child.pid
(record / f"{agent}.process.json").write_text(json.dumps(processes))
time.sleep(float(os.environ.get("FAKE_SLEEP", "0")))
rc = int(os.environ.get("FAKE_EXIT", "0"))
if rc:
    print("fake worker failure", file=sys.stderr)
raise SystemExit(rc)
