#!/usr/bin/env bash
# Install the sdlc-skills into an AI agent's skills folder.
#
#   install-skills.sh <agent-skills-folder>          copy every skill
#   install-skills.sh <agent-skills-folder> --link   link them to this clone, so `git pull` updates them
#
# A skill already in the folder is replaced only when it is a link or a folder
# with a SKILL.md (an earlier install); anything else stops the script first.
set -euo pipefail

usage() { echo "usage: $0 <agent-skills-folder> [--link]" >&2; exit 1; }
[ $# -ge 1 ] && [ $# -le 2 ] || usage
target=$1
mode=copy
if [ $# -eq 2 ]; then
  [ "$2" = "--link" ] || usage
  mode=link
fi
here=$(cd "$(dirname "$0")" && pwd)

skills=()
for dir in "$here"/skills/*/; do
  [ -f "$dir/SKILL.md" ] && skills+=("$(basename "$dir")")
done
[ ${#skills[@]} -gt 0 ] || { echo "error: no skills found in $here/skills" >&2; exit 1; }

for name in "${skills[@]}"; do
  dest="$target/$name"
  if [ -L "$dest" ] || [ ! -e "$dest" ] || { [ -d "$dest" ] && [ -f "$dest/SKILL.md" ]; }; then
    continue
  fi
  echo "error: $dest exists and is not an installed skill: move it away, then run again" >&2
  exit 1
done

mkdir -p "$target"
for name in "${skills[@]}"; do
  dest="$target/$name"
  rm -rf "$dest"
  if [ "$mode" = link ]; then
    ln -s "$here/skills/$name" "$dest"
    echo "linked $name -> $here/skills/$name"
  else
    cp -R "$here/skills/$name" "$dest"
    find "$dest" -name __pycache__ -type d -prune -exec rm -rf {} +
    echo "copied $name"
  fi
done
