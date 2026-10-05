#!/usr/bin/env bash
# Install the sdlc-skills into an AI agent.
#
#   install-skills.sh --agent claude            copy every skill
#   install-skills.sh --agent claude --link     link them to this clone, so `git pull` updates them
#   install-skills.sh --agent claude --agent codex   several agents at once
#   install-skills.sh --folder <dir>            an agent not listed: name its skills folder
#
# Run it with no arguments to list the supported agent names.
#
# A skill already in the folder is replaced only when it is a link or a folder
# with a SKILL.md (an earlier install); anything else stops the script first.
set -euo pipefail

# name | agent | its skills folder
AGENTS=(
  "claude|Claude Code|$HOME/.claude/skills"
  "codex|Codex|$HOME/.codex/skills"
  "gemini|Gemini CLI|$HOME/.gemini/skills"
  "cursor|Cursor|$HOME/.cursor/skills"
  "copilot|Copilot CLI|$HOME/.copilot/skills"
  "opencode|OpenCode|$HOME/.config/opencode/skills"
  "windsurf|Windsurf|$HOME/.codeium/windsurf/skills"
)

usage() {
  {
    echo "usage: $0 --agent <name> [--agent <name> ...] [--link]"
    echo
    echo "supported agents:"
    for entry in "${AGENTS[@]}"; do
      IFS='|' read -r name agent _ <<<"$entry"
      printf '  %-10s %s\n' "$name" "$agent"
    done
    echo
    echo "example: $0 --agent claude"
    echo
    echo "--link      link the skills to this clone instead of copying, so \`git pull\` updates them"
    echo "--folder    for an agent not listed: the folder it reads its skills from"
  } >&2
  exit 1
}

mode=copy
targets=()
while [ $# -gt 0 ]; do
  case $1 in
    --link) mode=link ;;
    --agent)
      [ $# -ge 2 ] || usage
      shift
      found=
      for entry in "${AGENTS[@]}"; do
        IFS='|' read -r name _ dir <<<"$entry"
        [ "$name" = "$1" ] && { targets+=("$dir"); found=1; }
      done
      [ -n "$found" ] || { echo "error: unknown agent '$1'" >&2; usage; }
      ;;
    --folder)
      [ $# -ge 2 ] || usage
      shift
      targets+=("$1")
      ;;
    *) usage ;;
  esac
  shift
done
[ ${#targets[@]} -gt 0 ] || usage
here=$(cd "$(dirname "$0")" && pwd)

skills=()
for dir in "$here"/skills/*/; do
  [ -f "$dir/SKILL.md" ] && skills+=("$(basename "$dir")")
done
[ ${#skills[@]} -gt 0 ] || { echo "error: no skills found in $here/skills" >&2; exit 1; }

for target in "${targets[@]}"; do
  for name in "${skills[@]}"; do
    dest="$target/$name"
    if [ -L "$dest" ] || [ ! -e "$dest" ] || { [ -d "$dest" ] && [ -f "$dest/SKILL.md" ]; }; then
      continue
    fi
    echo "error: $dest exists and is not an installed skill: move it away, then run again" >&2
    exit 1
  done
done

for target in "${targets[@]}"; do
  echo "installing into $target"
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
done
