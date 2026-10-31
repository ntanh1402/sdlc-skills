#!/usr/bin/env bash
# Build a scratch setup for one forward-test scenario:
#   <dir>/remote.git   a bare remote
#   <dir>/shop-wiki    a Wiki repository holding the sample Bundle, pushed to the remote
#   <dir>/workspace    a Workspace whose AGENTS.md links ../shop-wiki
#   <dir>/<source>     a made-up Import source, for --source with a folder
#   <dir>/<code>       a code repository with the remote <dir>/<code>.git, for --code
# Usage: forward-tests/seed.sh <dir> [--empty] [--fixture <name>]... [--source <name>]... [--change <source>:<name>]...
#                              [--code <name>]... [--merged <code>:<name>[:<Task key>]]...
#   --empty           an Application "shop" with no concepts instead of the sample
#   --fixture <name>  copy forward-tests/fixtures/<name>/ over wiki/ before the first commit
#   --source <name>   copy forward-tests/sources/<name>: a folder becomes the git repository
#                     <dir>/<name> with the remote URL https://github.com/acme/<name>.git;
#                     a file goes to <dir>/workspace/docs/ with the files that share its name
#   --change <source>:<name>  in <dir>/<source>, commit forward-tests/changes/<name>.patch on a
#                     new branch feat/<name>: a code change to review
#   --code <name>     copy the folder forward-tests/sources/<name> as the git repository <dir>/<name>
#                     and push it to a bare remote <dir>/<name>.git, whose default branch is main:
#                     a code repository to build a Task in and to close a Task from
#   --merged <code>:<name>[:<Task key>]  in <dir>/<code>, commit forward-tests/changes/<name>.patch
#                     on main and push it: merged code. With a Task key the commit message ends
#                     with the trailer "Task: <Task key>"
set -euo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
DIR="${1:?usage: forward-tests/seed.sh <dir> [--empty] [--fixture <name>]... [--source <name>]... [--change <source>:<name>]... [--code <name>]... [--merged <code>:<name>[:<Task key>]]...}"
shift
EMPTY=no
FIXTURES=()
SOURCES=()
CHANGES=()
CODES=()
MERGED=()
while [ $# -gt 0 ]; do
  case "$1" in
    --empty) EMPTY=yes; shift ;;
    --fixture) FIXTURES+=("${2:?--fixture needs a name}"); shift 2 ;;
    --source) SOURCES+=("${2:?--source needs a name}"); shift 2 ;;
    --change) CHANGES+=("${2:?--change needs <source>:<name>}"); shift 2 ;;
    --code) CODES+=("${2:?--code needs a name}"); shift 2 ;;
    --merged) MERGED+=("${2:?--merged needs <code>:<name>[:<Task key>]}"); shift 2 ;;
    *) echo "unknown option $1" >&2; exit 2 ;;
  esac
done
TOOL="python3 $HERE/skills/sdlc-setup-wiki/wiki-llm/tools/wiki_llm.py"
for name in "${SOURCES[@]}"; do
  [ -e "$HERE/forward-tests/sources/$name" ] || { echo "no such source: forward-tests/sources/$name" >&2; exit 2; }
done
for change in "${CHANGES[@]}"; do
  [ -f "$HERE/forward-tests/changes/${change#*:}.patch" ] || { echo "no such change: forward-tests/changes/${change#*:}.patch" >&2; exit 2; }
done
for name in "${CODES[@]}"; do
  [ -d "$HERE/forward-tests/sources/$name" ] || { echo "no such code folder: forward-tests/sources/$name" >&2; exit 2; }
done
for merged in "${MERGED[@]}"; do
  IFS=: read -r _ patch _ <<< "$merged"
  [ -f "$HERE/forward-tests/changes/$patch.patch" ] || { echo "no such change: forward-tests/changes/$patch.patch" >&2; exit 2; }
done
AUTHOR=(-c user.name="Forward Tester" -c user.email="tester@example.com")
[ -e "$DIR" ] && { echo "$DIR exists; choose a new folder" >&2; exit 1; }
mkdir -p "$DIR"
DIR="$(cd "$DIR" && pwd)"
WIKI="$DIR/shop-wiki"

git init -q --bare "$DIR/remote.git"
if [ "$EMPTY" = yes ]; then
  $TOOL init "$WIKI" --app shop --title "Shop Platform" --owner-team platform > /dev/null
  git -C "$WIKI" init -q
else
  mkdir "$WIKI"
  git -C "$WIKI" init -q
  cp -R "$HERE/forward-tests/sample" "$WIKI/wiki"
  $TOOL copy install "$WIKI" > /dev/null
  printf '.worktrees/\n__pycache__/\n' > "$WIKI/.gitignore"
fi
for name in "${FIXTURES[@]}"; do
  cp -R "$HERE/forward-tests/fixtures/$name/." "$WIKI/wiki/"
done
(cd "$WIKI" && python3 .wiki-llm/tools/wiki_llm.py sync > /dev/null)
(cd "$WIKI" && python3 .wiki-llm/tools/wiki_llm.py validate > /dev/null) || { echo "seeded wiki does not validate" >&2; exit 1; }

git -C "$WIKI" symbolic-ref HEAD refs/heads/main
if [ -z "$(git -C "$WIKI" config user.email || true)" ]; then
  git -C "$WIKI" config user.name "Forward Tester"
  git -C "$WIKI" config user.email "tester@example.com"
fi
git -C "$WIKI" add -A
git -C "$WIKI" commit -qm "Seed the forward-test wiki"
git -C "$WIKI" remote add origin "$DIR/remote.git"
git -C "$WIKI" push -q -u origin main
git -C "$WIKI" remote set-head origin main

mkdir "$DIR/workspace"
$TOOL link "$DIR/workspace" "$WIKI" > /dev/null
echo "wiki:      $WIKI"
echo "workspace: $DIR/workspace"

for name in "${SOURCES[@]}"; do
  from="$HERE/forward-tests/sources/$name"
  if [ -d "$from" ]; then
    cp -R "$from" "$DIR/$name"
    git -C "$DIR/$name" init -q
    git -C "$DIR/$name" symbolic-ref HEAD refs/heads/main
    git -C "$DIR/$name" add -A
    git -C "$DIR/$name" "${AUTHOR[@]}" commit -qm "Made-up source for the forward tests"
    git -C "$DIR/$name" remote add origin "https://github.com/acme/$name.git"
    echo "source:    $DIR/$name"
  else
    mkdir -p "$DIR/workspace/docs"
    cp "${from%.*}".* "$DIR/workspace/docs/"
    echo "source:    $DIR/workspace/docs/$name"
  fi
done
for name in "${CODES[@]}"; do
  repo="$DIR/$name"
  cp -R "$HERE/forward-tests/sources/$name" "$repo"
  git init -q --bare "$repo.git"
  git -C "$repo" init -q
  git -C "$repo" symbolic-ref HEAD refs/heads/main
  git -C "$repo" config user.name "Forward Tester"
  git -C "$repo" config user.email "tester@example.com"
  git -C "$repo" add -A
  git -C "$repo" commit -qm "Made-up code for the forward tests"
  git -C "$repo" remote add origin "$repo.git"
  git -C "$repo" push -q -u origin main
  git -C "$repo" remote set-head origin main
  echo "code:      $repo (remote $repo.git)"
done
for change in "${CHANGES[@]}"; do
  repo="$DIR/${change%%:*}"
  name="${change#*:}"
  git -C "$repo" checkout -q -b "feat/$name"
  git -C "$repo" apply "$HERE/forward-tests/changes/$name.patch"
  git -C "$repo" add -A
  git -C "$repo" "${AUTHOR[@]}" commit -qm "$name"
  echo "change:    $repo on branch feat/$name"
done
for merged in "${MERGED[@]}"; do
  IFS=: read -r code patch task <<< "$merged"
  repo="$DIR/$code"
  git -C "$repo" checkout -q main
  git -C "$repo" apply "$HERE/forward-tests/changes/$patch.patch"
  git -C "$repo" add -A
  if [ -n "$task" ]; then
    git -C "$repo" commit -qm "$patch" -m "Task: $task"
  else
    git -C "$repo" commit -qm "$patch"
  fi
  git -C "$repo" push -q origin main
  echo "merged:    $patch on main of $repo${task:+, Task: $task}"
done
