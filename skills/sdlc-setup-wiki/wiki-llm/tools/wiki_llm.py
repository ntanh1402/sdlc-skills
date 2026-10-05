#!/usr/bin/env python3
"""Command line for an SDLC Skills wiki bundle.

Every command prints JSON and exits 0 on success, 1 on a failed check, and 2 on
a usage or environment problem (no bundle, a schema mismatch, not a git repository).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from wikilib import coverage, docs, draft, link, locate, rename, scaffold, sync, toolcopy, validate
from wikilib.bundle import Bundle
from wikilib.errors import Refused, ToolError
from wikilib.schema import Schema


def locate_root(explicit: str | None, check_version: bool = True) -> Path:
    """--root, then WIKI_LLM_ROOT, then the bundle found by walking up from the
    current directory. The bundle must be of this tool's schema version."""
    root = locate.bundle_root(explicit or os.environ.get("WIKI_LLM_ROOT"), Path.cwd())
    if check_version:
        locate.check_version(root, Schema.load())
    return root


def _print(value: object) -> None:
    print(json.dumps(value, indent=2, ensure_ascii=False))


def cmd_validate(args: argparse.Namespace) -> int:
    result = validate.report(validate.run(locate_root(args.root)))
    _print(result)
    return 0 if result["ok"] else 1


def cmd_sync(args: argparse.Namespace) -> int:
    root = locate_root(args.root)
    bundle = Bundle.load(root, Schema.load())
    rendered, _, skipped_paths = sync.plan(bundle)
    skipped = [bundle.rel(path) for path in skipped_paths]
    if args.check:
        paths = [bundle.rel(path) for path in sync.stale(bundle, rendered)]
        _print({"ok": not paths, "stale": paths, "skipped": skipped})
        return 1 if paths else 0
    changed = [bundle.rel(path) for path in sync.write(root)]
    _print({"ok": True, "written": changed, "skipped": skipped})
    return 0


def cmd_docs(args: argparse.Namespace) -> int:
    schema = Schema.load()
    if args.check:
        stale = [path.name for path in docs.stale(schema)]
        broken = [f"{path.name}: {target}" for path, target in docs.broken_links()]
        _print({"ok": not stale and not broken, "stale": stale, "broken_links": broken})
        return 1 if stale or broken else 0
    changed = [path.name for path in docs.write(schema)]
    missing = [path.name for path, text in docs.render(schema).items() if text is None]
    _print({"ok": not missing, "written": changed, "missing_markers": missing})
    return 1 if missing else 0


def cmd_rename(args: argparse.Namespace) -> int:
    root = locate_root(args.root)
    result = rename.rename(
        root, args.old, args.new, app=args.app, change=args.change, allow_merged=args.allow_merged
    )
    _print(result)
    return 0


def cmd_coverage(args: argparse.Namespace) -> int:
    bundle = Bundle.load(locate_root(args.root), Schema.load())
    type_name, key = ("Feature", args.feature) if args.feature else ("ChangeRequest", args.change)
    result = coverage.report(bundle, args.what, type_name, key)
    _print(result)
    return 0 if result["ok"] else 1


def _report(result: dict) -> int:
    _print(result)
    return 0 if result["ok"] else 1


def cmd_draft(args: argparse.Namespace) -> int:
    here = Path.cwd()
    if args.action == "start":
        return _report(draft.start(here, args.key, args.branch))
    if args.action == "resume":
        return _report(draft.resume(here, args.key, args.branch))
    if args.action == "finish":
        return _report(draft.finish(here, args.by, args.verified_by, unverified=tuple(args.unverified)))
    if args.action == "diff":
        return _report(draft.diff(here))
    if args.action == "commit":
        return _report(draft.commit(here, args.message))
    return _report(draft.discard(here, args.key, args.branch, args.remote))


def cmd_refresh(args: argparse.Namespace) -> int:
    return _report(draft.refresh(Path.cwd()))


def cmd_verify(args: argparse.Namespace) -> int:
    return _report(draft.verify(Path.cwd(), args.path, args.by))


def cmd_init(args: argparse.Namespace) -> int:
    return _report(scaffold.init(Path(args.dir), args.app, args.title, args.owner_team))


def cmd_app(args: argparse.Namespace) -> int:
    return _report(scaffold.add_app(locate_root(args.root), args.key, args.title, args.owner_team))


def cmd_copy(args: argparse.Namespace) -> int:
    if args.action == "install":
        return _report(toolcopy.install(Path(args.dir)))
    repo = Path(args.dir) if args.dir else toolcopy.find(Path.cwd())
    if not (repo / toolcopy.COPY_DIR / toolcopy.MANIFEST).is_file():
        raise ToolError(f"no tool copy found in {repo}: run sdlc-setup-wiki to create the wiki repository")
    return _report(toolcopy.check(repo, Path(args.source) if args.source else None, args.release))


def cmd_link(args: argparse.Namespace) -> int:
    return _report(link.link(Path(args.workspace), Path(args.wiki)))


def cmd_migrate(args: argparse.Namespace) -> int:
    root = locate_root(args.root, check_version=False)
    found, current = locate.schema_version(root), Schema.load().version
    if found == current:
        _print({"ok": True, "from": found, "to": current, "written": []})
        return 0
    _print({"ok": False, "error": f"no migration from schema {found} to {current} is available in this version"})
    return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", help="bundle root (default: $WIKI_LLM_ROOT, then found by walking up from here)")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("validate", help="check the bundle against schema.json").set_defaults(run=cmd_validate)
    sync_parser = commands.add_parser("sync", help="write indexes and generated sections")
    sync_parser.add_argument("--check", action="store_true", help="report stale files without writing")
    sync_parser.set_defaults(run=cmd_sync)
    docs_parser = commands.add_parser("docs", help="write the generated tables of the schema pages")
    docs_parser.add_argument("--check", action="store_true", help="report stale pages and broken links without writing")
    docs_parser.set_defaults(run=cmd_docs)
    rename_parser = commands.add_parser("rename", help="rename a concept or Requirement and every reference to it")
    rename_parser.add_argument("old")
    rename_parser.add_argument("new")
    rename_parser.add_argument("--app", help="the application, when the key exists in several")
    rename_parser.add_argument("--change", help="rename a Requirement only inside this ChangeRequest")
    rename_parser.add_argument(
        "--allow-merged", action="store_true", help="rename a key already on the default branch (migrations only)"
    )
    rename_parser.set_defaults(run=cmd_rename)
    coverage_parser = commands.add_parser("coverage", help="what has no TestCase, no Task or no user story")
    coverage_parser.add_argument("what", choices=["tests", "tasks", "stories"])
    subject = coverage_parser.add_mutually_exclusive_group(required=True)
    subject.add_argument("--feature", help="a Feature key")
    subject.add_argument("--change", help="a ChangeRequest key")
    coverage_parser.set_defaults(run=cmd_coverage)
    draft_parser = commands.add_parser("draft", help="a branch and worktree holding unapproved changes")
    actions = draft_parser.add_subparsers(dest="action", required=True)
    for name, text in (("start", "create the draft branch wiki/<key> and its worktree"),
                       ("resume", "recreate the worktree of an existing draft branch"),
                       ("discard", "remove the worktree and delete the draft branch")):
        action = actions.add_parser(name, help=text)
        action.add_argument("key")
        action.add_argument("--branch", help="a branch name other than wiki/<key>")
        if name == "discard":
            action.add_argument("--remote", action="store_true", help="also delete the branch on the remote")
    finish_parser = actions.add_parser("finish", help="stamp provenance, check logs, sync and validate")
    finish_parser.add_argument("--by", required=True, help="the actor that wrote the changes")
    finish_parser.add_argument(
        "--verified-by", nargs="?", const="",
        help="a human:<id> who confirmed the changed files (without a value: from git config user.email)",
    )
    finish_parser.add_argument(
        "--unverified", nargs="+", default=[], metavar="PATH",
        help="with --verified-by: changed files, or folders of them, the person did not check; they get no verified stamp",
    )
    actions.add_parser("diff", help="the change set shown for approval")
    commit_parser = actions.add_parser("commit", help="commit, push and remove the worktree")
    commit_parser.add_argument("-m", "--message", required=True)
    draft_parser.set_defaults(run=cmd_draft)
    commands.add_parser("refresh", help="merge the default branch into the draft").set_defaults(run=cmd_refresh)
    verify_parser = commands.add_parser("verify", help="record that a person confirmed a file")
    verify_parser.add_argument("path")
    verify_parser.add_argument("--by", help="a human:<id> actor (default: from git config user.email)")
    verify_parser.set_defaults(run=cmd_verify)
    init_parser = commands.add_parser("init", help="write a new wiki repository skeleton with a tool copy")
    init_parser.add_argument("dir")
    init_parser.add_argument("--app", required=True, help="the Application key, e.g. shop")
    init_parser.add_argument("--title", required=True)
    init_parser.add_argument("--owner-team", required=True)
    init_parser.set_defaults(run=cmd_init)
    app_parser = commands.add_parser("app", help="add an application to the bundle")
    app_actions = app_parser.add_subparsers(dest="action", required=True)
    add_parser = app_actions.add_parser("add", help="write <app>/overview.md as init does, then sync")
    add_parser.add_argument("--key", required=True, help="the Application key, e.g. billing")
    add_parser.add_argument("--title", required=True)
    add_parser.add_argument("--owner-team", required=True)
    app_parser.set_defaults(run=cmd_app)
    copy_parser = commands.add_parser("copy", help="install or check the tool copy in .wiki-llm/")
    copy_actions = copy_parser.add_subparsers(dest="action", required=True)
    copy_actions.add_parser("install", help="replace <dir>/.wiki-llm/ with this tool").add_argument("dir")
    check_parser = copy_actions.add_parser("check", help="compare the tool copy with its manifest and a release")
    check_parser.add_argument("dir", nargs="?", help="the wiki repository (default: found by walking up)")
    against = check_parser.add_mutually_exclusive_group()
    against.add_argument("--source", help="a tool folder to compare versions with (default: this tool)")
    against.add_argument("--release", help="a Release version to compare with, e.g. the RELEASE file of a skill")
    copy_parser.set_defaults(run=cmd_copy)
    link_parser = commands.add_parser("link", help="write the note that tells a workspace's skills where the wiki is")
    link_parser.add_argument("workspace", help="the folder the AI agent is started in")
    link_parser.add_argument("wiki", help="the wiki repository")
    link_parser.set_defaults(run=cmd_link)
    commands.add_parser("migrate", help="bring a bundle to this tool's schema version").set_defaults(run=cmd_migrate)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.run(args)
    except Refused as error:
        _print({"ok": False, "error": str(error)})
        return 1
    except ToolError as error:
        _print({"ok": False, "error": str(error)})
        return 2


if __name__ == "__main__":
    sys.exit(main())
