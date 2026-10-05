"""Temporary git repositories for the commands that use git.

`GitTest` gives every test its own git configuration, so a developer's global
settings (signing, hooks, default branch) never reach the tool's git calls.
"""

from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from . import fixture


def git(cwd: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def commit_all(repo: Path, message: str = "change") -> str:
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", message)
    return git(repo, "rev-parse", "HEAD")


class GitTest(unittest.TestCase):
    """A wiki repository with the fixture bundle in wiki/, committed on main."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        config = self.tmp / "gitconfig"
        config.write_text(
            "[user]\n\tname = Test\n\temail = alice@example.com\n[init]\n\tdefaultBranch = main\n"
            "[commit]\n\tgpgsign = false\n",
            encoding="utf-8",
        )
        self._env = mock.patch.dict(os.environ, {"GIT_CONFIG_GLOBAL": str(config), "GIT_CONFIG_NOSYSTEM": "1"})
        self._env.start()
        os.environ.pop("WIKI_LLM_ROOT", None)
        self.repo = self.tmp / "acme-wiki"
        self.root = fixture.make_bundle(self.repo / "wiki")
        (self.repo / ".gitignore").write_text(".worktrees/\n__pycache__/\n", encoding="utf-8")
        git(self.repo, "init", "-q", "-b", "main")
        commit_all(self.repo, "initial")

    def tearDown(self) -> None:
        self._env.stop()
        self._tmp.cleanup()

    def add_remote(self) -> Path:
        """A bare repository as origin, with main pushed and origin/HEAD set."""
        remote = self.tmp / "origin.git"
        git(self.tmp, "init", "-q", "--bare", "-b", "main", str(remote))
        git(self.repo, "remote", "add", "origin", str(remote))
        git(self.repo, "push", "-q", "-u", "origin", "main")
        git(self.repo, "remote", "set-head", "origin", "main")
        return remote

    def clone(self, name: str) -> Path:
        """A second clone of origin, as another writer would have."""
        other = self.tmp / name
        git(self.tmp, "clone", "-q", str(self.tmp / "origin.git"), str(other))
        return other
