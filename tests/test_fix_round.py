#!/usr/bin/env python3
"""Offline regression checks for permission, ownership, lifecycle, and model review."""
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import time

from test_tools import ROOT, TEMP, RUNS, WORK, RECORDS, call, wrapper, launch, metadata, flag, quota_env, codex_quota, claude_quota, get_quota


def wait_for(predicate, seconds=8):
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        if predicate():
            return
        time.sleep(.02)
    raise AssertionError("Timed out waiting for the expected local test state")


def write_script(path, text):
    path.write_text(text)
    path.chmod(0o755)


def minimal_path(name):
    directory = TEMP / name
    directory.mkdir()
    for command in ("bash", "python3", "basename", "dirname", "readlink", "uname", "cat", "grep", "cut", "mkdir", "date", "mv", "head", "tail", "wc", "sort", "stat", "env", "ln", "mktemp", "git", "rm", "sleep", "chmod"):
        source = shutil.which(command)
        if source:
            (directory / command).symlink_to(source)
    for agent in ("codex", "claude"):
        (directory / agent).symlink_to(ROOT / "tests/fake_worker.py")
    return directory


def test_permission_and_metadata():
    path = minimal_path("no-sandbox-deps")
    for missing in ("bwrap", "socat"):
        other = "socat" if missing == "bwrap" else "bwrap"
        write_script(path / other, "#!/usr/bin/env bash\nexit 0\n")
        result = subprocess.run([str(ROOT / "bin/claude-task"), "run", "-s", "rw", "-p", "task"],
                                env=dict(os.environ, PATH=str(path)), capture_output=True, text=True, timeout=5)
        assert result.returncode == 2 and "bwrap and socat" in result.stderr and "sudo apt-get install bubblewrap socat" in result.stderr
        (path / other).unlink()
    wrapper("claude", "run", "-s", "rw", "-p", "task", env=dict(FAKE_SANDBOX_EXIT="1"), code=2)
    # Permissive user settings must not become worker arguments.
    settings = Path(os.environ["HOME"]) / ".claude/settings.json"
    settings.parent.mkdir(exist_ok=True)
    settings.write_text(json.dumps(dict(permissions=dict(allow=["Bash(*)"]), sandbox=dict(enabled=False))))
    run, _, args, _ = launch("claude", "run", "-n", "safe-config", "-s", "ro", "-C", WORK, "-p", "task")
    assert flag(args, "--setting-sources") == "" and json.loads(flag(args, "--settings"))["sandbox"] == dict(enabled=False)
    assert "--allowedTools" not in args
    for agent in ("codex", "claude"):
        before = set(RUNS.iterdir())
        result = subprocess.run([str(ROOT / "bin" / f"{agent}-task"), "run", "-n", "demo\nSANDBOX_SHORT=full", "-C", str(WORK), "-p", "task"], capture_output=True, text=True, timeout=5)
        assert result.returncode == 2 and "newlines" in result.stderr and set(RUNS.iterdir()) == before
        assert "Read-only reviewers cannot run test suites" in wrapper(agent, "--help")
    output = wrapper("claude", "run", "-t", "haiku", "-s", "ro", "-C", WORK, "-p", "task")
    assert "MODEL   haiku   SANDBOX ro (default)" in output and "haiku/" not in output
    assert "cannot run tests" in wrapper("claude", "--help") and "network blocked" in wrapper("claude", "--help")
    wrapper("claude", "watch", TEMP / "missing-run", ".01", "1", code=2)
    orphan = TEMP / "orphan"
    orphan.mkdir()
    (orphan / "meta.env").write_text(f"START={int(time.time())}\n")
    output = wrapper("claude", "watch", orphan, ".05", "1", code=1)
    assert "no worker pid" in output
    print("PASS: sandbox dependency refusal, isolated permissions, metadata injection, display/help, and abandoned watches")


def test_atomic_runs_and_search():
    path = TEMP / "collision-bin"
    path.mkdir()
    write_script(path / "date", '#!/usr/bin/env bash\nif [[ "${1:-}" == +%Y%m%d-%H%M%S ]]; then echo 20000101-000000; else exec /usr/bin/date "$@"; fi\n')
    for agent in ("codex", "claude"):
        processes = []
        for index in range(6):
            env = dict(os.environ, PATH=str(path) + os.pathsep + os.environ["PATH"], FAKE_RECORD_DIR=str(TEMP / f"parallel-record-{agent}-{index}"))
            process = subprocess.Popen([str(ROOT / "bin" / f"{agent}-task"), "run", "-n", "collision", "-C", str(WORK), "-p", f"task {index}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
            processes.append(process)
        allocated = []
        for index, process in enumerate(processes):
            output, errors = process.communicate(timeout=10)
            assert process.returncode == 0, errors
            run = Path(next(line[8:] for line in output.splitlines() if line.startswith("RUN     ")))
            allocated.append(run)
            assert run.name.startswith(f"20000101-000000-{agent}-collision")
            assert (run / "prompt.md").read_text().startswith(f"task {index}")
        assert len(set(allocated)) == len(processes)
    codex, _, _, _ = launch("codex", "run", "-n", "claude-audit", "-C", WORK, "--search", "-p", "task")
    for kind, extra in (("run", []), ("resume", [codex]), ("review", ["--base", "main"])):
        _, meta, args, _ = launch("codex", kind, *extra, "--search", "-n", "search-" + kind, "-C", WORK, "-p", "task")
        assert args[:2] == ["--search", "exec"] and meta["SEARCH"] == "1"
    claude, _, _, _ = launch("claude", "run", "-n", "codex-audit", "-C", WORK, "-p", "task")
    assert codex.name in wrapper("codex", "ls", "100") and claude.name not in wrapper("codex", "ls", "100")
    assert claude.name in wrapper("claude", "ls", "100") and codex.name not in wrapper("claude", "ls", "100")
    print("PASS: simultaneous run allocation, top-level search on run/resume/review, and exact agent listings")


def test_completion_and_signals():
    path = TEMP / "slow-parser-bin"
    path.mkdir()
    write_script(path / "python3", f'#!/usr/bin/env bash\nif [[ "${{2:-}}" == meta ]]; then sleep .4; fi\nexec "{sys.executable}" "$@"\n')
    for agent in ("codex", "claude"):
        name = "publish-" + agent
        process = subprocess.Popen([str(ROOT / "bin" / f"{agent}-task"), "run", "-n", name, "-C", str(WORK), "-p", "task"], env=dict(os.environ, PATH=str(path) + os.pathsep + os.environ["PATH"], FAKE_SLEEP=".2"), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            wait_for(lambda: bool(list(RUNS.glob(f"*-{agent}-{name}/pid"))))
            run = next(RUNS.glob(f"*-{agent}-{name}"))
            output = wrapper(agent, "watch", run, ".01", "10")
            assert "DONE exit=0" in output
            assert (run / "last.md").stat().st_size and metadata(run)["THREAD"]
            assert metadata(run)["EXIT"] == "0" and "END" in metadata(run)
            process.communicate(timeout=5)
            assert process.returncode == 0
        finally:
            if process.poll() is None:
                process.kill()
                process.communicate()
        for signum in (signal.SIGTERM, signal.SIGINT):
            name = f"signal-{agent}-{signum}"
            record = TEMP / name
            process = subprocess.Popen([str(ROOT / "bin" / f"{agent}-task"), "run", "-n", name, "-C", str(WORK), "-p", "task"], env=dict(os.environ, FAKE_RECORD_DIR=str(record), FAKE_SLEEP="60", FAKE_DESCENDANT="1"), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            try:
                wait_for(lambda: (record / f"{agent}.process.json").exists())
                pids = json.loads((record / f"{agent}.process.json").read_text())
                process.send_signal(signum)
                output, errors = process.communicate(timeout=8)
                assert process.returncode == 128 + signum, (output, errors)
                run = Path(next(line[8:] for line in output.splitlines() if line.startswith("RUN     ")))
                assert metadata(run)["EXIT"] == str(128 + signum) and (run / "exit_code").read_text().strip() == str(128 + signum)
                assert (run / "last.md").exists() and metadata(run)["END"]
                for pid in [int((run / "pid").read_text()), *pids.values()]:
                    try:
                        os.kill(pid, 0)
                    except ProcessLookupError:
                        pass
                    else:
                        raise AssertionError(f"Interrupted process {pid} survived or was not reaped")
            finally:
                if process.poll() is None:
                    process.kill()
                    process.communicate()
    print("PASS: complete archives before DONE, SIGTERM/SIGINT forwarding, and reaped escaped descendants")


def test_parser_and_quota_regressions():
    parser = ROOT / "lib/agent_events.py"
    file = TEMP / "malformed-fields.jsonl"
    original = (ROOT / "tests/fixtures/codex-events.jsonl").read_text()
    malformed = [dict(type="item.completed", item=dict(type="file_change", changes=1)), dict(type="item.completed", item=dict(type="todo_list", items=1))]
    file.write_text(original + "\n".join(json.dumps(event) for event in malformed))
    assert call("python3", parser, "meta", "codex", file) == call("python3", parser, "meta", "codex", ROOT / "tests/fixtures/codex-events.jsonl")
    for mode in ("items", "last", "final"):
        call("python3", parser, mode, "codex", file)
    for agent, events in (
        ("codex", [dict(type="item.completed", item=dict(type="command_execution", command="first\n\tsecond\rthird", exit_code=0)), dict(type="item.completed", item=dict(type="file_change", changes=[dict(kind="update", path="a\nb")]))]),
        ("claude", [dict(type="assistant", message=dict(content=[dict(type="tool_use", name="Bash", input=dict(command="first\n\tsecond\rthird"))])), dict(type="assistant", message=dict(content=[dict(type="tool_use", name="multi\ntool", input={})])), dict(type="assistant", message=dict(content=1))])
    ):
        file.write_text("\n".join(json.dumps(event) for event in events))
        items = call("python3", parser, "items", agent, file, "20")
        assert len(items.splitlines()) == 2 and "first second third" in items and "\t" not in items and "\r" not in items
        assert len(call("python3", parser, "last", agent, file).splitlines()) == 1
    unknown, meta, _, _ = launch("codex", "review", "-n", "zero-unknown", "-C", WORK, "-p", "review", env=dict(FAKE_ZERO_USAGE="1"))
    assert all(meta[key] == "unknown" for key in ("TOKENS_IN", "TOKENS_CACHED", "TOKENS_OUT", "TOKENS_REASONING"))
    rollout = Path(os.environ["HOME"]) / ".codex/sessions/2000/01/01/rollout-fake-token-counts.jsonl"
    rollout.parent.mkdir(parents=True, exist_ok=True)
    rollout.write_text(json.dumps(dict(type="session_meta", payload=dict(id=meta["THREAD"]))) + "\n" + json.dumps(dict(type="event_msg", payload=dict(type="token_count", info=dict(last_token_usage=dict(input_tokens=1234, cached_input_tokens=345, output_tokens=22, reasoning_output_tokens=17))))))
    _, meta, _, _ = launch("codex", "review", "-n", "zero-rollout", "-C", WORK, "-p", "review", env=dict(FAKE_ZERO_USAGE="1"))
    assert [meta[key] for key in ("TOKENS_IN", "TOKENS_CACHED", "TOKENS_OUT", "TOKENS_REASONING")] == ["1234", "345", "22", "17"]
    env = quota_env("retained-week")
    codex_quota(env, 10, 50)
    weekly = claude_quota(env, 10, 50, seven_day=True)
    event = json.loads(weekly.read_text().splitlines()[0])
    event["rate_limit_info"]["unifiedWindows"] = dict(seven_day=dict(utilization=.95, resetsAt=time.time() + 302400))
    weekly.write_text(json.dumps(event))
    os.utime(weekly, (time.time() - 500, time.time() - 500))
    newest = claude_quota(env, 10, 50, name="20000102-000000-claude-newest")
    result = get_quota(env)
    windows = result["claude"]["windows"]
    assert windows["seven_day"]["status"] == "critical" and windows["seven_day"]["source"] == str(weekly) and windows["seven_day"]["age_seconds"] >= 500
    assert windows["five_hour"]["source"] == str(newest) and "Claude >90%" in result["advice"]
    print("PASS: malformed event fields, whitespace, zero-token rollout fallback, and retained per-window Claude observations")


def test_install_dependencies():
    path = minimal_path("installer-no-deps")
    home = TEMP / "dependency-install-home"
    home.mkdir()
    repo = TEMP / "dependency-install-repo"
    repo.mkdir()
    shutil.copy(ROOT / "install.sh", repo / "install.sh")
    shutil.copytree(ROOT / "bin", repo / "bin")
    result = subprocess.run(["bash", str(repo / "install.sh")], env=dict(os.environ, HOME=str(home), PATH=str(path)), capture_output=True, text=True, timeout=5)
    assert result.returncode == 0 and "sudo apt-get install bubblewrap socat" in result.stderr, (result.stdout, result.stderr)
    assert not (home / ".claude/skills/agents-playbook").is_symlink()  # This checkout has no shipped skill.
    print("PASS: Linux dependency warnings and skipped missing skill sources in a temporary HOME")


def test_model_review():
    env = quota_env("model-review")
    root = Path(env["AGENT_RUNS_ROOT"])
    state = root / "model-review"
    state.mkdir()
    cache = Path(env["HOME"]) / ".codex/models_cache.json"
    cache.parent.mkdir(parents=True)
    def models(ids):
        cache.write_text(json.dumps(dict(identity="must-not-be-copied", models=[dict(slug=model, display_name=model.title(), description="fake capability", supported_reasoning_levels=[dict(effort="low", description="cheap")], default_reasoning_level="low", private_field="must-not-be-copied") for model in ids])))
    models(["fake-sol", "fake-reserve"])
    fake_bin = TEMP / "research-fake-bin"
    fake_bin.mkdir()
    record = TEMP / "research-record.jsonl"
    finished = TEMP / "research-finished"
    env.update(PATH=str(fake_bin) + os.pathsep + os.environ["PATH"], MODEL_REVIEW_RECORD=str(record), MODEL_REVIEW_FINISHED=str(finished))
    write_script(fake_bin / "codex-task", '''#!/usr/bin/env python3
import json,os,sys,time
from pathlib import Path
record=dict(argv=sys.argv[1:],prompt=sys.stdin.read(),run=os.environ["AGENT_RUN_DIR"],pid=os.getpid(),sid=os.getsid(0))
with open(os.environ["MODEL_REVIEW_RECORD"],"a") as output: output.write(json.dumps(record)+"\\n")
time.sleep(2.5)
Path(os.environ["MODEL_REVIEW_FINISHED"]).write_text("done")
''')
    (state / "last-check").write_text(str(time.time()))
    assert call(ROOT / "bin/model-review", "--if-stale", "--claude-models", "fake-sonnet,fake-opus", env=env) == ""
    assert not (state / "snapshot.json").exists() and not record.exists()
    (state / "last-check").write_text(str(time.time() - 4 * 86400))
    for index, (exit_code, status, seconds, tokens_in, tokens_out) in enumerate(((0, "done", 10, 10, 1), (2, "done", 30, 30, 3), (0, "partial", 20, "unknown", 5))):
        run = root / f"20000101-000000-codex-stat-{index}"
        run.mkdir()
        (run / "meta.env").write_text(f"AGENT=codex\nMODEL=demo\nEFFORT=low\nEXIT={exit_code}\nSTART=100\nEND={100+seconds}\nTOKENS_IN={tokens_in}\nTOKENS_OUT={tokens_out}\n")
        (run / "last.md").write_text(f"STATUS: {status}\n")
    assert call(ROOT / "bin/model-review", "--if-stale", "3", "--claude-models", "fake-sonnet,fake-opus", "--dry-run", env=env) == ""
    facts = next(state.glob("*/facts.md"))
    text = facts.read_text()
    assert "fake-reserve, fake-sol" in text and "fake-opus, fake-sonnet" in text
    assert "| codex | demo | low | 3 | 2 | 20 | 20 | 3 |" in text
    assert "must-not-be-copied" not in text and not record.exists()
    stamp = facts.stat().st_mtime_ns
    assert call(ROOT / "bin/model-review", "--if-stale", "0", "--claude-models", "fake-opus,fake-sonnet", env=env) == ""
    assert facts.stat().st_mtime_ns == stamp and not record.exists()
    models(["fake-sol", "fake-luna"])
    assert call(ROOT / "bin/model-review", "--if-stale", "0", "--claude-models", "fake-sonnet,fake-haiku", "--dry-run", env=env) == ""
    text = facts.read_text()
    for line in ("Codex added: fake-luna", "Codex removed: fake-reserve", "Claude added: fake-haiku", "Claude removed: fake-opus"):
        assert line in text
    assert not record.exists()
    # Force overrides a fresh marker; the research worker outlives the checker.
    start = time.monotonic()
    output = call(ROOT / "bin/model-review", "--force", env=env)
    assert time.monotonic() - start < 2 and output.startswith("model-review: 0 model change(s); research run ") and len(output.splitlines()) == 1
    wait_for(record.exists)
    records = [json.loads(line) for line in record.read_text().splitlines()]
    assert len(records) == 1
    observed = records[0]
    assert observed["argv"] == ["run", "--search", "-n", "model-review", "-t", "sol", "-e", "high", "-s", "ro", "-C", str(ROOT)]
    assert observed["pid"] == observed["sid"] and not finished.exists()
    assert str(facts) in observed["prompt"] and str(ROOT / "playbook/models.md") in observed["prompt"] and str(ROOT / "playbook/routing.md") in observed["prompt"]
    assert "last 30 days" in observed["prompt"] and "at most 10 lines" in observed["prompt"]
    assert call(ROOT / "bin/model-review", "--if-stale", env=env) == ""
    wait_for(finished.exists)
    # Exercise the real wrapper integration with the fake Codex binary.
    (fake_bin / "codex-task").unlink()
    (fake_bin / "codex-task").symlink_to(ROOT / "bin/codex-task")
    env["FAKE_RECORD_DIR"] = str(TEMP / "research-wrapper-records")
    models(["fake-sol", "fake-astra"])
    output = call(ROOT / "bin/model-review", "--if-stale", "0", env=env)
    assert output.startswith("model-review: 2 model change(s);")
    run = Path(output.strip().split("research run ", 1)[1])
    wait_for(lambda: (run / "exit_code").exists())
    assert (run / "exit_code").read_text().strip() == "0" and metadata(run)["SEARCH"] == "1" and metadata(run)["AGENT"] == "codex"
    args = json.loads((Path(env["FAKE_RECORD_DIR"]) / "codex.argv.json").read_text())
    assert args[:2] == ["--search", "exec"] and (run / "research.log").exists()
    print("PASS: model-review freshness, diffs, silent unchanged checks, statistics, dry-run, and one detached research worker")


test_permission_and_metadata()
test_atomic_runs_and_search()
test_completion_and_signals()
test_parser_and_quota_regressions()
test_install_dependencies()
test_model_review()
print("All fix-round offline tests passed.")
