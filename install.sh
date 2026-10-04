#!/usr/bin/env bash
# Link the current checkout into each CLI's skills directory and ~/.local/bin.
set -euo pipefail

REPO_ROOT="$(dirname "$(readlink -f "$0")")"
mode=install
case "${1:-}" in
  --uninstall) mode=uninstall ;;
  -h | --help) echo "Usage: install.sh [--uninstall]"; exit 0 ;;
  "") ;;
  *) echo "install.sh: unknown option '$1'" >&2; exit 2 ;;
esac
(($# <= 1)) || { echo "Usage: install.sh [--uninstall]" >&2; exit 2; }

link_target() {
  local source="$1" target="$2" current
  if [[ "$mode" == uninstall ]]; then
    if [[ -L "$target" ]]; then
      current="$(readlink -m "$target")"
      if [[ "$current" == "$REPO_ROOT/"* ]]; then
        rm -- "$target"
        echo "Removed $target"
      fi
    fi
    return
  fi
  mkdir -p "$(dirname "$target")"
  if [[ -L "$target" ]] && [[ "$(readlink -m "$target")" == "$source" ]]; then
    return
  fi
  if [[ -e "$target" && ! -L "$target" ]]; then
    local backup="$target.bak-$(date +%Y%m%d-%H%M%S)"
    [[ -e "$backup" || -L "$backup" ]] && backup="$backup-$$"
    mv -- "$target" "$backup"
    echo "Backed up $target to $backup"
  fi
  ln -sfn -- "$source" "$target"
  echo "Linked $target"
}

link_target "$REPO_ROOT/skills/claude/codex-collab" "$HOME/.claude/skills/codex-collab"
if [[ -d "$HOME/.codex" || "$mode" == uninstall ]]; then
  link_target "$REPO_ROOT/skills/codex/claude-collab" "$HOME/.codex/skills/claude-collab"
fi
for source in "$REPO_ROOT"/bin/*; do
  [[ -f "$source" ]] || continue
  link_target "$source" "$HOME/.local/bin/$(basename "$source")"
done

if [[ "$mode" == install ]]; then
  for command in codex claude python3 git; do
    command -v "$command" >/dev/null 2>&1 || echo "Warning: $command is not installed or not on PATH." >&2
  done
  if [[ -f /etc/os-release ]] && grep -Eq '^ID="?ubuntu"?$' /etc/os-release &&
     [[ "$(cat /proc/sys/kernel/apparmor_restrict_unprivileged_userns 2>/dev/null || true)" == 1 ]] &&
     [[ ! -e /etc/apparmor.d/bwrap ]]; then
    cat <<'FIX'
Warning: Ubuntu restricts unprivileged user namespaces and has no bwrap AppArmor profile.
A human must approve this security-policy change. Run these commands only after approval:
sudo apt-get install bubblewrap
sudo tee /etc/apparmor.d/bwrap >/dev/null <<'PROFILE'
abi <abi/4.0>,
include <tunables/global>
profile bwrap /usr/bin/bwrap flags=(unconfined) {
  userns,
}
PROFILE
sudo apparmor_parser -r /etc/apparmor.d/bwrap
FIX
  fi
fi
