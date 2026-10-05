#!/usr/bin/env python3
"""Check local converter executables and print install guidance."""

from __future__ import annotations

import argparse
import importlib.metadata
import shutil
import sys


TOOLS = {
    "markitdown": {
        "command": "markitdown",
        "distribution": "markitdown",
        "version": "0.1.6",
        "install": "python -m pip install 'markitdown[all]==0.1.6'",
    },
    "marker": {
        "command": "marker_single",
        "distribution": "marker-pdf",
        "version": "1.10.2",
        "install": "python -m pip install 'marker-pdf==1.10.2'",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check dependencies for document-to-Markdown conversion"
    )
    parser.add_argument(
        "--engine",
        choices=("auto", "all", "markitdown", "marker"),
        default="auto",
        help="Dependencies to check (auto and all check both)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    selected = (
        ("markitdown", "marker") if args.engine in {"auto", "all"} else (args.engine,)
    )
    missing = []
    print(f"Python: {sys.version.split()[0]}")
    if sys.version_info < (3, 10):
        print("  MISSING: Python 3.10 or newer is required")
        missing.append("python")

    for name in selected:
        tool = TOOLS[name]
        path = shutil.which(tool["command"])
        try:
            installed_version = importlib.metadata.version(tool["distribution"])
        except importlib.metadata.PackageNotFoundError:
            installed_version = None

        if path and installed_version == tool["version"]:
            print(f"{name}: OK {installed_version} ({path})")
        elif path and installed_version is not None:
            print(
                f"{name}: VERSION MISMATCH {installed_version} "
                f"(expected {tool['version']}, executable {path})"
            )
            print(f"  Install: {tool['install']}")
            missing.append(name)
        elif path:
            print(
                f"{name}: UNVERIFIED VERSION (expected {tool['version']}, "
                f"executable {path})"
            )
            print(f"  Install into this Python environment: {tool['install']}")
            missing.append(name)
        else:
            print(f"{name}: MISSING {tool['version']} ({tool['command']})")
            print(f"  Install: {tool['install']}")
            if name == "marker":
                print(
                    "  For DOCX/PPTX/XLSX/HTML/EPUB inputs: "
                    "python -m pip install 'marker-pdf[full]==1.10.2'"
                )
            missing.append(name)

    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
