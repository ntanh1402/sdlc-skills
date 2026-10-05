"""The git steps the tool takes. Every call goes through `run`."""

from __future__ import annotations

import subprocess
from pathlib import Path

from .errors import ToolError


def run(cwd: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    """Run git in `cwd`. A failing command raises ToolError unless `check` is False."""
    result = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    if check and result.returncode != 0:
        message = (result.stderr or result.stdout).strip()
        raise ToolError(f"git {' '.join(args)} failed: {message}")
    return result


def out(cwd: Path, *args: str) -> str:
    return run(cwd, *args).stdout.strip()


def ok(cwd: Path, *args: str) -> bool:
    return run(cwd, *args, check=False).returncode == 0


def is_repository(path: Path) -> bool:
    return path.is_dir() and ok(path, "rev-parse", "--is-inside-work-tree")


def toplevel(path: Path) -> Path:
    """The working tree root that contains `path`."""
    if not is_repository(path):
        raise ToolError(f"not a git repository: {path}")
    return Path(out(path, "rev-parse", "--show-toplevel"))


def has_remote(cwd: Path, name: str = "origin") -> bool:
    return name in out(cwd, "remote").split()


def has_ref(cwd: Path, ref: str) -> bool:
    return ok(cwd, "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}")


def default_branch(cwd: Path) -> str:
    """The base of every Draft: the remote's default branch, else a local main,
    else a local master."""
    remote_head = run(cwd, "symbolic-ref", "--quiet", "refs/remotes/origin/HEAD", check=False)
    if remote_head.returncode == 0:
        return remote_head.stdout.strip().removeprefix("refs/remotes/")
    for name in ("main", "master"):
        if has_ref(cwd, f"refs/heads/{name}"):
            return name
    raise ToolError("no default branch: the repository has no origin/HEAD, main or master")


def exists_at(cwd: Path, ref: str, path: str) -> bool:
    """True when `path` (relative to the repository root) exists at `ref`."""
    return ok(cwd, "cat-file", "-e", f"{ref}:{path}")


def show(cwd: Path, ref: str, path: str) -> str | None:
    """The text of `path` at `ref`, or None when it does not exist there."""
    result = run(cwd, "show", f"{ref}:{path}", check=False)
    return result.stdout if result.returncode == 0 else None

