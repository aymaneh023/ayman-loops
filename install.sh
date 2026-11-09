#!/usr/bin/env bash
# Links every skill in skills/ into Claude Code. Safe to run again: it skips links that exist.
set -euo pipefail
repo="$(cd "$(dirname "$0")" && pwd)"
root="$HOME/.claude/skills"
mkdir -p "$root"

for skill in "$repo"/skills/*/; do
  name="$(basename "$skill")"
  link="$root/$name"
  if [ -e "$link" ] || [ -L "$link" ]; then
    # Leave a real folder alone; it is not ours to replace.
    [ -L "$link" ] || echo "skip $link (exists, not a link)" >&2
    continue
  fi
  ln -s "${skill%/}" "$link"
  echo "linked $link"
done
