"""Run every rule module in wikilib.rules against a bundle."""

from __future__ import annotations

import importlib
import pkgutil
from pathlib import Path

from . import rules
from .bundle import Bundle, Finding
from .schema import Schema


def rule_modules() -> list:
    """Rule modules sorted by their ORDER constant. Each exposes check(bundle)."""
    modules = [
        importlib.import_module(f"{rules.__name__}.{info.name}")
        for info in pkgutil.iter_modules(rules.__path__)
    ]
    return sorted(modules, key=lambda module: (module.ORDER, module.__name__))


def run(root: Path, schema: Schema | None = None) -> list[Finding]:
    bundle = Bundle.load(root, schema or Schema.load())
    findings: list[Finding] = []
    for module in rule_modules():
        findings.extend(module.check(bundle))
    unique = sorted(set(findings), key=lambda item: (item.path, item.rule, item.message))
    return unique


def report(findings: list[Finding]) -> dict:
    def rows(severity: str) -> list[dict]:
        return [
            {"rule": item.rule, "path": item.path, "message": item.message}
            for item in findings
            if item.severity == severity
        ]

    errors = rows("error")
    return {"ok": not errors, "errors": errors, "warnings": rows("warning")}
