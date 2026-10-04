#!/usr/bin/env python3
"""Offline worker: record the call, then replay a captured event stream."""
import json
import os
from pathlib import Path
import sys

agent = Path(sys.argv[0]).name
if agent not in ("codex", "claude"):
    raise SystemExit("Invoke this fake through a codex or claude symlink")
record = Path(os.environ["FAKE_RECORD_DIR"])
record.mkdir(parents=True, exist_ok=True)
args = sys.argv[1:]
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
sys.stdout.write(events)
rc = int(os.environ.get("FAKE_EXIT", "0"))
if rc:
    print("fake worker failure", file=sys.stderr)
raise SystemExit(rc)
