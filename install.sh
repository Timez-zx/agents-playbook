#!/usr/bin/env bash
# Link shipped skills and commands without replacing unrelated symlinks.
set -euo pipefail
REPO_ROOT="$(dirname "$(readlink -f "$0")")"
mode=install with_codex=0 backup_root=""
usage() {
  cat <<'HELP'
Usage: install.sh [--with-codex-front] [--uninstall]
  --with-codex-front  Also install the optional Codex front skill.
  --uninstall        Remove exact links owned by this checkout, including both front skills.
Existing files/directories move to ~/.agent-runs/install-backups/<stamp>/<original-relative-path>.
Unrelated symlinks are preserved. No packages or scheduled jobs are installed.
HELP
}
while (($#)); do
  case "$1" in
    --with-codex-front) with_codex=1 ;;
    --uninstall) mode=uninstall ;;
    -h | --help) usage; exit 0 ;;
    *) echo "install.sh: unknown option '$1'" >&2; exit 2 ;;
  esac
  shift
done

link_target() {
  local source="$1" target="$2" current
  if [[ -L "$target" ]]; then
    current="$(readlink -m "$target")"
    if [[ "$current" == "$source" ]]; then
      if [[ "$mode" == uninstall ]]; then rm -- "$target"; echo "Removed $target"; fi
    else
      echo "Warning: preserving unrelated symlink $target -> $(readlink "$target")" >&2
    fi
    return
  fi
  [[ "$mode" == install ]] || return 0
  [[ -e "$source" ]] || { echo "Warning: source missing; preserving $target: $source" >&2; return 0; }
  mkdir -p "$(dirname "$target")"
  if [[ -e "$target" ]]; then
    if [[ -z "$backup_root" ]]; then
      mkdir -p "$HOME/.agent-runs/install-backups"
      backup_root="$(mktemp -d "$HOME/.agent-runs/install-backups/$(date +%Y%m%d-%H%M%S)-XXXXXX")"
    fi
    local backup="$backup_root/${target#"$HOME/"}"
    mkdir -p "$(dirname "$backup")"
    mv -- "$target" "$backup"
    echo "Backed up $target to $backup"
  fi
  ln -s -- "$source" "$target"
  echo "Linked $target"
}

link_skill() {
  local agent="$1" source="$REPO_ROOT/skills/$1/agents-playbook" target="$HOME/.$1/skills/agents-playbook"
  if [[ "$mode" == install ]]; then
    [[ -d "$source" ]] || { echo "Warning: shipped skill missing: $source; existing target preserved" >&2; return 0; }
    if [[ ! -L "$source/repo" || "$(readlink "$source/repo" 2>/dev/null || true)" != ../../.. || "$(readlink -f "$source/repo" 2>/dev/null || true)" != "$REPO_ROOT" ]]; then
      echo "Warning: $source/repo must be a shipped relative symlink resolving to this repo; existing target preserved" >&2
      return 0
    fi
  fi
  link_target "$source" "$target"
}
link_skill claude
if ((with_codex)) || [[ "$mode" == uninstall ]]; then link_skill codex; fi
for source in "$REPO_ROOT"/bin/*; do
  [[ -f "$source" ]] || continue
  link_target "$source" "$HOME/.local/bin/$(basename "$source")"
done

if [[ "$mode" == install ]]; then
  for command in codex claude python3 git; do
    command -v "$command" >/dev/null 2>&1 || echo "Warning: $command is not installed or not on PATH." >&2
  done
  if [[ "$(uname -s)" == Linux ]]; then
    missing=()
    command -v bwrap >/dev/null 2>&1 || missing+=(bubblewrap)
    command -v socat >/dev/null 2>&1 || missing+=(socat)
    if ((${#missing[@]})); then
      echo "Warning: Claude rw sandbox dependencies are missing. A human can run: sudo apt-get install ${missing[*]}" >&2
    fi
  fi
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
