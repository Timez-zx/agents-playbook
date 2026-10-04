#!/usr/bin/env python3
"""Integration checks for the public CLI, with fake workers only."""
import json
import os
import shutil
import signal
from pathlib import Path
import subprocess
import select
import sys
import time

ROOT, TEMP = map(Path, sys.argv[1:])
RUNS = Path(os.environ["AGENT_RUNS_ROOT"])
RECORDS = Path(os.environ["FAKE_RECORD_DIR"])
GUARD = "You are a worker. Do not delegate to other agents and do not run codex-task or claude-task."
META_KEYS = "NAME KIND AGENT MODEL EFFORT SANDBOX SANDBOX_SHORT NET CWD PARENT START END EXIT THREAD TOKENS_IN TOKENS_CACHED TOKENS_OUT TOKENS_REASONING".split()
WORK = TEMP / "work tree"
WORK.mkdir(exist_ok=True)


def call(*args, stdin=None, env=None, code=0):
    result = subprocess.run([str(a) for a in args], input=stdin, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            env={k: v for k, v in dict(os.environ, **(env or {})).items() if v is not None}, timeout=15)
    assert result.returncode == code, (args, result.returncode, result.stdout, result.stderr)
    return result.stdout


def wrapper(agent, *args, **kwargs):
    return call(ROOT / "bin" / f"{agent}-task", *args, **kwargs)


def launch(agent, *args, **kwargs):
    output = wrapper(agent, *args, **kwargs)
    run = Path(next(line[8:] for line in output.splitlines() if line.startswith("RUN     ")))
    assert run.parent == RUNS
    assert f"-{agent}-" in run.name
    for filename in "prompt.md events.jsonl stderr.log last.md meta.env pid exit_code".split():
        assert (run / filename).is_file(), filename
    meta = metadata(run)
    assert all(key in meta for key in META_KEYS), meta
    assert meta["AGENT"] == agent and meta["EXIT"] == (run / "exit_code").read_text().strip()
    assert int(meta["END"]) >= int(meta["START"])
    argv = json.loads((RECORDS / f"{agent}.argv.json").read_text())
    prompt = (RECORDS / f"{agent}.stdin.txt").read_text()
    worker_env = json.loads((RECORDS / f"{agent}.env.json").read_text())
    assert worker_env == dict(AGENT_ROLE="worker", CWD=meta["CWD"]), worker_env
    assert prompt == (run / "prompt.md").read_text()
    if agent == "codex":
        assert sum(line.startswith("Codex:") for line in output.splitlines()) == 1
    return run, meta, argv, prompt


def metadata(run):
    return dict(line.split("=", 1) for line in (run / "meta.env").read_text().splitlines())


def flag(argv, name):
    return argv[argv.index(name) + 1]


def assert_permissions(argv, mode):
    assert flag(argv, "--permission-mode") == dict(ro="default", rw="acceptEdits", full="bypassPermissions")[mode]
    denied = set(flag(argv, "--disallowedTools").split(","))
    assert {"Task", "Agent"} <= denied
    assert denied == ({"Task", "Agent", "Edit", "Write", "NotebookEdit"} if mode == "ro" else {"Task", "Agent"})
    if mode == "full":
        assert "--settings" not in argv
    else:
        sandbox = dict(enabled=False) if mode == "ro" else dict(enabled=True, autoAllowBashIfSandboxed=True, failIfUnavailable=True, allowUnsandboxedCommands=False)
        assert json.loads(flag(argv, "--settings")) == dict(sandbox=sandbox)
        assert flag(argv, "--setting-sources") == "" and flag(argv, "--permission-prompts") == "none"
        assert "--strict-mcp-config" in argv and json.loads(flag(argv, "--mcp-config")) == dict(mcpServers={})


def test_wrappers():
    initial = {}
    prompt_file = TEMP / "input.md"
    prompt_file.write_text("file input\nsecond line\n")
    for agent in ("codex", "claude"):
        wrapper(agent, "--help")
        run, meta, argv, prompt = launch(agent, "run", "-n", "first", "-C", WORK, "-p", "implement it")
        initial[agent] = run
        assert GUARD in prompt and "STATUS: done | partial | blocked" in prompt
        assert meta["NAME"] == "first" and meta["KIND"] == "run" and meta["PARENT"] == ""
        assert meta["SANDBOX_SHORT"] == "ro" and meta["NET"] == "0" and meta["CWD"] == str(WORK)
        if agent == "codex":
            assert argv[:2] == ["exec", "--json"]
            assert flag(argv, "-m") == meta["MODEL"] == "gpt-6.1-sol"
            assert meta["EFFORT"] == "high"
            assert 'sandbox_mode="read-only"' in argv
            assert (meta["TOKENS_IN"], meta["TOKENS_CACHED"], meta["TOKENS_OUT"]) == ("89566", "82432", "1008")
            assert meta["THREAD"] == "00000000-0000-4000-8000-000000000001"
            assert (run / "last.md").read_text().startswith("STATUS: done")
        else:
            assert argv[:4] == ["-p", "--output-format", "stream-json", "--verbose"]
            assert flag(argv, "--model") == meta["MODEL"] == "sonnet"
            assert flag(argv, "--effort") == meta["EFFORT"] == "medium"
            assert_permissions(argv, "ro")
            assert (meta["TOKENS_IN"], meta["TOKENS_CACHED"], meta["TOKENS_OUT"], meta["TOKENS_REASONING"]) == ("62666", "53439", "173", "88")
            assert meta["THREAD"] == "00000000-0000-4000-8000-000000000002"
            assert meta["COST_USD"] == "0.0246459"
            assert meta["CLAUDE_UTIL_FIVE_HOUR"] == "0.11" and meta["CLAUDE_RESETS_FIVE_HOUR"] == "1791156600"
            assert (run / "last.md").read_text() == "PONG\n"
        _, resumed, args, text = launch(agent, "resume", run, "-p", "continue")
        assert resumed["PARENT"] == str(run) and resumed["THREAD"] == meta["THREAD"]
        assert resumed["MODEL"] == meta["MODEL"] and resumed["CWD"] == str(WORK)
        assert resumed["NAME"] == "first-followup" and GUARD in text
        if agent == "codex":
            assert args[:2] == ["exec", "resume"] and args[-2:] == [meta["THREAD"], "-"]
        else:
            assert flag(args, "--resume") == meta["THREAD"]
        raw_run, raw_meta, _, text = launch(agent, "run", "-n", "raw", "-C", WORK, "--raw", "-f", prompt_file)
        assert text == prompt_file.read_text() and "Handoff contract" not in text and raw_meta["RAW"] == "1"
        _, _, _, text = launch(agent, "resume", raw_run, "-p", "fix one line")
        assert text.strip() == "fix one line", repr(text[:300])  # raw is inherited on resume
        _, _, _, text = launch(agent, "run", "-n", "stdin", "-C", WORK, stdin="stdin input")
        assert text.startswith("stdin input") and GUARD in text
        for target, value, phrase in (("--uncommitted", None, "staged, unstaged and untracked"), ("--base", "main", "git diff main...HEAD"), ("--commit", "deadbeef", "git show deadbeef")):
            options = [target] + ([value] if value else [])
            _, review_meta, args, text = launch(agent, "review", "-n", target[2:], "-C", WORK, "-s", "full", *options, "-p", "check failures")
            assert phrase in text and "check failures" in text and "NO FINDINGS" in text
            assert review_meta["SANDBOX_SHORT"] == "ro" and review_meta["KIND"] == "review"
            assert target not in args  # targets plus custom prompts must always be folded
            if agent == "claude":
                assert_permissions(args, "ro")
            else:
                assert args[:3] == ["exec", "review", "--json"]
        _, _, args, text = launch(agent, "review", "-n", "default-review", "-C", WORK, stdin="")
        if agent == "codex":
            assert "--uncommitted" in args and "-" not in args and text == "\n"
        else:
            assert "Review the uncommitted changes" in text and "NO FINDINGS" in text
        _, _, _, text = launch(agent, "review", "-n", "raw-review", "-C", WORK, "--base", "main", "--raw", "-p", "check it")
        assert "git diff main...HEAD" in text and "Reporting format" not in text
        peek = wrapper(agent, "peek", run, "2").splitlines()
        assert len(peek) == 2 and all(line.startswith("[") for line in peek)
        assert wrapper(agent, "watch", run, "0.01", "1").startswith("DONE exit=0 events=")
        listing = wrapper(agent, "ls", "100")
        assert run.name in listing and "exit=0" in listing
        assert f"-{'claude' if agent == 'codex' else 'codex'}-" not in listing
        if agent == "codex":
            assert "STATUS: done" in listing
        failed, failed_meta, _, _ = launch(agent, "run", "-n", "failed", "-C", WORK, "-p", "fail", env={"FAKE_EXIT": "7"}, code=7)
        assert failed_meta["EXIT"] == "7" and (failed / "stderr.log").read_text().strip() == "fake worker failure"
    print("PASS: both wrappers run/resume/review/peek/watch/ls, metadata, contracts, worker role, and failures")
    return initial


def test_flags():
    for tier, model, effort in (("luna", "gpt-6-luna", "medium"), ("reserve", "gpt-reserve", "medium"), ("sol", "gpt-6.1-sol", "high"), ("astra", "gpt-6-astra", "xhigh")):
        _, meta, args, _ = launch("codex", "run", "-n", tier, "-C", WORK, "-t", tier, "-p", "task")
        assert meta["MODEL"] == model and meta["EFFORT"] == effort and flag(args, "-m") == model
    for tier, effort in (("haiku", ""), ("sonnet", "medium"), ("opus", "high")):
        _, meta, args, _ = launch("claude", "run", "-n", tier, "-C", WORK, "-t", tier, "-p", "task")
        assert meta["MODEL"] == tier and meta["EFFORT"] == effort
        if effort:
            assert flag(args, "--effort") == effort
        else:
            assert "--effort" not in args
            run = Path(next(p for p in RUNS.glob("*-claude-haiku") if metadata(p)["MODEL"] == "haiku"))
            _, meta, args, _ = launch("claude", "resume", run, "-p", "follow up")
            assert meta["EFFORT"] == "" and "--effort" not in args
            _, meta, args, _ = launch("claude", "resume", run, "-t", "opus", "-p", "escalate")
            assert meta["MODEL"] == "opus" and flag(args, "--effort") == "high"
    for agent in ("codex", "claude"):
        for mode in ("ro", "rw", "full"):
            _, meta, args, _ = launch(agent, "run", "-n", mode, "-C", WORK, "-s", mode, "-m", "custom-model", "-e", "low", "--add-dir", WORK, "--add-dir", TEMP, "-p", "task")
            assert meta["MODEL"] == "custom-model" and meta["EFFORT"] == "low" and meta["SANDBOX_SHORT"] == mode
            assert args.count("--add-dir") == 2
            if agent == "claude":
                assert_permissions(args, mode)
            else:
                assert f'sandbox_mode="{dict(ro="read-only", rw="workspace-write", full="danger-full-access")[mode]}"' in args
    _, meta, args, _ = launch("codex", "run", "-n", "net", "-C", WORK, "-s", "rw", "--net", "-p", "task")
    assert meta["NET"] == "1" and "sandbox_workspace_write.network_access=true" in args
    result = subprocess.run([str(ROOT / "bin/claude-task"), "run", "--net", "-p", "task"], capture_output=True, text=True, timeout=10)
    assert result.returncode == 2 and "--net is not supported" in result.stderr and "-s full" in result.stderr
    print("PASS: tier defaults, explicit overrides, add-dir, permissions, and network handling")


def test_watch_and_defaults():
    for agent in ("codex", "claude"):
        run = TEMP / f"{agent}-watch"
        run.mkdir()
        (run / "meta.env").write_text(f"START={int(time.time())}\n")
        (run / "pid").write_text(str(os.getpid()))
        fixture = "codex-events.jsonl" if agent == "codex" else "claude-stream.jsonl"
        (run / "events.jsonl").write_text((ROOT / "tests/fixtures" / fixture).read_text())
        process = subprocess.Popen([str(ROOT / "bin" / f"{agent}-task"), "watch", str(run), "0.1", "2"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            assert select.select([process.stdout], [], [], 5)[0], "no heartbeat"
            assert process.stdout.readline().startswith("HB elapsed=")
            os.utime(run / "events.jsonl", (time.time() - 10, time.time() - 10))
            for _ in range(5):
                assert select.select([process.stdout], [], [], 5)[0], "no stall notice"
                if process.stdout.readline().startswith("STALL no new events"):
                    break
            else:
                raise AssertionError("watch did not detect stale events")
            (run / "completed").write_text("0\n")
            (run / "completed").rename(run / "exit_code")
            output, errors = process.communicate(timeout=5)
            assert process.returncode == 0 and "DONE exit=0" in output, (output, errors)
        finally:
            if process.poll() is None:
                process.kill()
                process.communicate()
        output = wrapper(agent, "run", "-n", "default-root", "-C", WORK, "-p", "task", env={"AGENT_RUNS_ROOT": None})
        default_run = Path(next(line[8:] for line in output.splitlines() if line.startswith("RUN     ")))
        assert default_run.parent == Path(os.environ["HOME"]) / ".agent-runs"
    print("PASS: watch heartbeat/stall/completion and the default shared runs root")


def test_parser():
    parser = ROOT / "lib/agent_events.py"
    for agent, fixture in (("codex", "codex-events.jsonl"), ("claude", "claude-stream.jsonl")):
        text = (ROOT / "tests/fixtures" / fixture).read_text()
        damaged = TEMP / f"{agent}-damaged.jsonl"
        damaged.write_text('not-json\n[]\nnull\n' + text + '{"type":')
        clean = call("python3", parser, "meta", agent, ROOT / "tests/fixtures" / fixture)
        assert call("python3", parser, "meta", agent, damaged) == clean
        items = call("python3", parser, "items", agent, damaged, "100")
        assert "[msg]" in items and "[cmd]" in items
        final = call("python3", parser, "final", agent, damaged)
        assert final.startswith("STATUS: done") if agent == "codex" else final == "PONG\n"
        assert call("python3", parser, "last", agent, damaged).startswith("events=")
        assert call("python3", parser, "last", agent, TEMP / "missing") == "events=0 last=(none yet)\n"
        assert call("python3", parser, "items", agent, damaged, "0") == ""
    custom = TEMP / "claude-custom.jsonl"
    custom.write_text('\n'.join(json.dumps(e) for e in [
        dict(type="assistant", message=dict(content=[dict(type="thinking", thinking="line one\nline two"), dict(type="tool_use", name="Write", input=dict(file_path="a.py")), dict(type="tool_use", name="TodoWrite", input=dict(todos=[])), dict(type="tool_use", name="Read", input=dict(file_path="a.py"))])),
        dict(type="user", message=dict(content=[dict(type="tool_result", is_error=True, content="failed\nresult")])),
        dict(type="rate_limit_event", rate_limit_info=dict(unifiedWindows=dict(seven_day=dict(utilization=.25, resetsAt=123)))),
        dict(type="result", session_id="fake", result="final error", is_error=True, usage=dict(input_tokens=2, output_tokens=3), total_cost_usd=.1),
    ]))
    items = call("python3", parser, "items", "claude", custom, "100")
    for marker in ("[think] line one line two", "[file] Write a.py", "[todo]", "[tool] Read", "[result] error failed result", "[done] error final error"):
        assert marker in items, items
    assert len(items.splitlines()) == 3  # One summary per event, even with several content blocks.
    assert call("python3", parser, "last", "claude", custom).startswith("events=3 last=[done]")
    meta = call("python3", parser, "meta", "claude", custom)
    assert "CLAUDE_UTIL_SEVEN_DAY=0.25" in meta and "CLAUDE_RESETS_SEVEN_DAY=123" in meta
    print("PASS: event parsing, final messages, all event summaries, and partial/invalid lines")


def quota_env(case):
    home, runs = TEMP / f"quota-{case}-home", TEMP / f"quota-{case}-runs"
    home.mkdir(exist_ok=True)
    runs.mkdir(exist_ok=True)
    return dict(HOME=str(home), AGENT_RUNS_ROOT=str(runs))


def codex_quota(env, used, elapsed, secondary=False):
    path = Path(env["HOME"]) / ".codex/sessions/2000/01/01/rollout-fake.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    now = time.time()
    values = dict(used_percent=used, window_minutes=10080, resets_at=now + (1 - elapsed / 100) * 604800)
    limits = dict(limit_id="fake", primary=values, plan_type="fake-plan", credits=dict(balance="fake-balance"))
    if secondary:
        limits["secondary"] = dict(used_percent=5, window_minutes=300, resets_at=now + 9000)
    path.write_text(json.dumps(dict(payload=dict(rate_limits=dict(primary=dict(used_percent=99))))) + '\n' + json.dumps(dict(type="event_msg", payload=dict(type="token_count", rate_limits=limits))) + '\n{"partial":')
    return path


def claude_quota(env, used, elapsed, name="20000101-000000-claude-fake", seven_day=False):
    path = Path(env["AGENT_RUNS_ROOT"]) / name / "events.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    now = time.time()
    windows = dict(five_hour=dict(utilization=used / 100, resetsAt=now + (1 - elapsed / 100) * 18000))
    if seven_day:
        windows["seven_day"] = dict(utilization=.05, resetsAt=now + 302400)
    path.write_text(json.dumps(dict(type="rate_limit_event", rate_limit_info=dict(unifiedWindows=windows))) + '\n{"partial":')
    return path


def get_quota(env):
    return json.loads(call(ROOT / "bin/agent-quota", "--json", env=env))


def test_quota():
    for status, used, elapsed in (("healthy", 10, 50), ("over-burning", 45, 10), ("high", 80, 70), ("critical", 95, 50), ("healthy", 70, 50), ("high", 90, 80)):
        env = quota_env(f"{status}-{used}")
        codex_quota(env, used, elapsed, secondary=True)
        claude_quota(env, used, elapsed, seven_day=True)
        result = get_quota(env)
        for agent, key in (("codex", "primary"), ("claude", "five_hour")):
            data = result[agent]["windows"][key]
            assert data["status"] == status, result
            assert data["used_percent"] == used
            assert abs(data["elapsed_percent"] - elapsed) < .1
        assert result["codex"]["plan_type"] == "fake-plan"
        assert result["codex"]["credits"]["balance"] == "fake-balance"
        assert result["codex"]["windows"]["secondary"]["window_seconds"] == 18000
        assert result["claude"]["windows"]["seven_day"]["window_seconds"] == 604800
        output = call(ROOT / "bin/agent-quota", env=env)
        assert "record age" in output and "Routing:" in output
        line = call(ROOT / "bin/agent-quota", "--codex-line", env=env)
        assert len(line.splitlines()) == 1 and line.startswith("Codex:")
        if status == "healthy":
            assert result["advice"] == "Use default routing."
        elif status == "critical":
            assert "tell the user" in result["advice"] and "critical-path" in result["advice"]
        else:
            assert "Scout and Writer" in result["advice"] and "Claude sonnet" in result["advice"]
    env = quota_env("missing")
    result = get_quota(env)
    assert not result["codex"]["windows"] and not result["claude"]["windows"]
    assert result["codex"]["errors"] and result["claude"]["errors"]
    output = call(ROOT / "bin/agent-quota", env=env)
    assert "unknown" in output and "get_usage" in output and "claude-task run -t haiku" in output
    env = quota_env("newest")
    old = codex_quota(env, 95, 50)
    os.utime(old, (time.time() - 120, time.time() - 120))
    newest = old.with_name("rollout-newest.jsonl")
    newest.write_text(json.dumps(dict(payload=dict(rate_limits=dict(primary=dict(used_percent=5, window_minutes=300, resets_at=time.time() + 9000))))))
    stream = claude_quota(env, 15, 50)
    os.utime(stream, (time.time() - 120, time.time() - 120))
    no_rate = Path(env["AGENT_RUNS_ROOT"]) / "20000102-000000-claude-no-rate/events.jsonl"
    no_rate.parent.mkdir()
    no_rate.write_text('{"type":"result","result":"no quota"}\n')
    result = get_quota(env)
    assert result["codex"]["source"] == str(newest) and result["codex"]["windows"]["primary"]["used_percent"] == 5
    assert result["claude"]["source"] == str(stream) and result["claude"]["age_seconds"] >= 120
    newer = claude_quota(env, 95, 50, name="20000103-000000-claude-newer")
    assert get_quota(env)["claude"]["source"] == str(newer)
    newest.write_text('invalid\n{"payload":{"rate_limits":null}}\n')
    fallback = get_quota(env)["codex"]
    assert fallback["source"] == str(old) and fallback["windows"]["primary"]["used_percent"] == 95
    old.write_text('{"payload":{}}\n')
    assert not get_quota(env)["codex"]["windows"]
    env = quota_env("critical-routing")
    codex_quota(env, 80, 50)
    claude_quota(env, 95, 50)
    result = get_quota(env)
    assert "tell the user" in result["advice"] and "Shift routine Executor work to Claude" not in result["advice"]
    env["AGENT_RUNS_ROOT"] = str(Path(env["HOME"]) / ".agent-runs")
    claude_quota(env, 10, 50)
    result = get_quota(dict(env, AGENT_RUNS_ROOT=""))
    assert result["claude"]["windows"]["five_hour"]["used_percent"] == 10
    print("PASS: quota states, thresholds, burn rate, routing, newest files, age, and missing/corrupt files")


def test_install():
    repo = TEMP / "install-repo"
    repo.mkdir()
    shutil.copy(ROOT / "install.sh", repo / "install.sh")
    shutil.copytree(ROOT / "bin", repo / "bin")
    shutil.copytree(ROOT / "lib", repo / "lib")
    for agent in ("claude", "codex"):
        skill = repo / "skills" / agent / "agents-playbook"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("Offline skill fixture")
        (skill / "repo").symlink_to("../../..", target_is_directory=True)
    home = Path(os.environ["HOME"])
    claude_skill = home / ".claude/skills/agents-playbook"
    claude_skill.mkdir(parents=True)
    (claude_skill / "old.txt").write_text("old skill")
    bin_dir = home / ".local/bin"
    bin_dir.mkdir(parents=True)
    old_binary = bin_dir / "codex-task"
    old_binary.write_text("old binary")
    installer = repo / "install.sh"
    help_text = call("bash", installer, "--help")
    assert "--with-codex-front" in help_text and "--uninstall" in help_text
    call("bash", installer)
    codex_skill = home / ".codex/skills/agents-playbook"
    assert not codex_skill.exists() and not codex_skill.is_symlink()
    call("bash", installer, "--with-codex-front")
    targets = [claude_skill, codex_skill] + [bin_dir / name for name in ("codex-task", "claude-task", "agent-quota", "model-review")]
    for target in targets:
        assert target.is_symlink() and target.exists() and str(target.readlink()).startswith(str(repo) + "/")
    backup_base = home / ".agent-runs/install-backups"
    backup_dirs = list(backup_base.iterdir())
    assert len(backup_dirs) == 1
    assert (backup_dirs[0] / ".local/bin/codex-task").read_text() == "old binary"
    assert (backup_dirs[0] / ".claude/skills/agents-playbook/old.txt").read_text() == "old skill"
    assert not list((home / ".claude/skills").glob("*.bak-*"))
    call("bash", installer, "--with-codex-front")
    assert list(backup_base.iterdir()) == backup_dirs
    call(bin_dir / "codex-task", "run", "-n", "installed", "-C", WORK, "-p", "task")
    call(bin_dir / "claude-task", "run", "-n", "installed", "-C", WORK, "-p", "task")
    call(bin_dir / "agent-quota", "--json")
    protected = bin_dir / "claude-task"
    protected.unlink()
    protected.symlink_to(repo / "bin/codex-task")  # Same repo, wrong expected source: still foreign.
    codex_skill.unlink()
    codex_skill.mkdir()
    (codex_skill / "keep.txt").write_text("keep regular directory")
    call("bash", installer, "--with-codex-front")
    assert protected.readlink() == repo / "bin/codex-task"
    assert (backup_base / next(p.name for p in backup_base.iterdir() if p != backup_dirs[0]) / ".codex/skills/agents-playbook/keep.txt").is_file()
    call("bash", installer, "--uninstall")
    for target in (claude_skill, codex_skill, bin_dir / "codex-task", bin_dir / "agent-quota", bin_dir / "model-review"):
        assert not target.exists() and not target.is_symlink()
    assert protected.is_symlink() and protected.readlink() == repo / "bin/codex-task"
    call("bash", installer, "--uninstall")
    for case in ("missing", "broken"):
        isolated_home = TEMP / ("installer-" + case)
        target = isolated_home / ".claude/skills/agents-playbook"
        target.mkdir(parents=True)
        (target / "keep.txt").write_text("keep")
        source = repo / "skills/claude/agents-playbook"
        if case == "missing":
            source.rename(source.with_name("saved"))
        else:
            (source / "repo").unlink()
            (source / "repo").symlink_to("../../missing")
        result = subprocess.run(["bash", str(installer)], env=dict(os.environ, HOME=str(isolated_home)), capture_output=True, text=True)
        assert result.returncode == 0 and "Warning:" in result.stderr and (target / "keep.txt").is_file()
        if case == "missing":
            source.with_name("saved").rename(source)
    foreign_home = TEMP / "installer-foreign"
    foreign = foreign_home / ".local/bin/codex-task"
    foreign.parent.mkdir(parents=True)
    foreign.symlink_to("/opt/custom/codex-task")
    call("bash", installer, env=dict(HOME=str(foreign_home)))
    assert foreign.readlink() == Path("/opt/custom/codex-task")
    call("bash", installer, "--uninstall", env=dict(HOME=str(foreign_home)))
    assert foreign.is_symlink()
    call("bash", installer, "--cron", code=2)
    print("PASS: installer skill sources/repo links, optional front, external backups, foreign links, and safe uninstall")


if __name__ == "__main__":
    test_wrappers()
    test_flags()
    test_watch_and_defaults()
    test_parser()
    test_quota()
    test_install()
    print("All baseline offline tests passed.")
