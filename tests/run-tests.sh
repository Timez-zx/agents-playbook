#!/usr/bin/env bash
# Everything runs against temporary homes and fake workers, with no network.
set -euo pipefail
ROOT="$(dirname "$(dirname "$(readlink -f "$0")")")"
TEST_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/agent-tools-tests.XXXXXX")"
trap 'rm -rf -- "$TEST_ROOT"' EXIT
export HOME="$TEST_ROOT/home"
export AGENT_RUNS_ROOT="$TEST_ROOT/agent runs"
export FAKE_RECORD_DIR="$TEST_ROOT/records"
export FIXTURES_DIR="$ROOT/tests/fixtures"
mkdir -p "$HOME" "$TEST_ROOT/fake-bin" "$FAKE_RECORD_DIR"
ln -s "$ROOT/tests/fake_worker.py" "$TEST_ROOT/fake-bin/codex"
ln -s "$ROOT/tests/fake_worker.py" "$TEST_ROOT/fake-bin/claude"
for dependency in bwrap socat; do
  printf '#!/usr/bin/env bash\nexit "${FAKE_SANDBOX_EXIT:-0}"\n' > "$TEST_ROOT/fake-bin/$dependency"
  chmod +x "$TEST_ROOT/fake-bin/$dependency"
done
export PATH="$TEST_ROOT/fake-bin:$PATH"
# Do not inherit worker CLI configuration from the machine running the tests.
unset CODEX_RUNS_ROOT
for script in "$ROOT"/bin/codex-task "$ROOT"/bin/claude-task "$ROOT"/install.sh; do
  bash -n "$script"
done
while IFS= read -r -d '' script; do
  bash -n "$script"
done < <(find "$ROOT/tests" -type f -name '*.sh' -print0)
if command -v shellcheck >/dev/null 2>&1; then
  shellcheck "$ROOT/bin/codex-task" "$ROOT/bin/claude-task" "$ROOT/install.sh" "$ROOT/tests/run-tests.sh"
else
  echo 'shellcheck: not installed (skipped)'
fi
python3 "$ROOT/tests/test_tools.py" "$ROOT" "$TEST_ROOT"
python3 "$ROOT/tests/test_fix_round.py" "$ROOT" "$TEST_ROOT"
