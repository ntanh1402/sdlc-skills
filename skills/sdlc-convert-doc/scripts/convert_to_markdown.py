#!/usr/bin/env python3
"""Route local document conversion through MarkItDown or Marker."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


IMAGE_SUFFIXES = {
    ".bmp",
    ".gif",
    ".jpeg",
    ".jpg",
    ".png",
    ".tif",
    ".tiff",
    ".webp",
}
MARKER_SUFFIXES = IMAGE_SUFFIXES | {
    ".docx",
    ".epub",
    ".htm",
    ".html",
    ".pdf",
    ".pptx",
    ".xlsx",
}
MARKDOWN_SUFFIXES = {".md", ".markdown"}


class ConversionError(RuntimeError):
    """Report a conversion or routing failure without a traceback."""


@dataclass(frozen=True)
class ConversionPlan:
    engine: str
    reason: str
    force_ocr: bool = False
    pdf_ocr_fallback: bool = False


def non_negative_int(value: str) -> int:
    number = int(value)
    if number < 0:
        raise argparse.ArgumentTypeError("must be zero or greater")
    return number


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Convert a local document to Markdown with MarkItDown or Marker. "
            "Auto mode uses Marker for images and as an OCR fallback for PDFs."
        )
    )
    parser.add_argument("input", type=Path, help="Local source document")
    parser.add_argument("-o", "--output", type=Path, help="Destination .md file")
    parser.add_argument(
        "--engine",
        choices=("auto", "markitdown", "marker"),
        default="auto",
        help="Converter selection (default: auto)",
    )
    parser.add_argument(
        "--ocr-threshold",
        type=non_negative_int,
        default=80,
        metavar="CHARS",
        help=(
            "For auto-routed PDFs, retry with Marker when MarkItDown emits fewer "
            "than this many alphanumeric characters; 0 disables the quality fallback "
            "(default: 80)"
        ),
    )
    ocr_group = parser.add_mutually_exclusive_group()
    ocr_group.add_argument(
        "--force-ocr",
        action="store_true",
        help="Use Marker and OCR the entire document",
    )
    ocr_group.add_argument(
        "--strip-existing-ocr",
        action="store_true",
        help="Use Marker, remove existing OCR text, and preserve digital text",
    )
    parser.add_argument(
        "--page-range",
        help='Marker page indexes, for example "0,5-10,20"',
    )
    parser.add_argument(
        "--use-llm",
        action="store_true",
        help="Enable Marker's configured LLM service",
    )
    parser.add_argument(
        "--disable-image-extraction",
        action="store_true",
        help="Tell Marker not to save extracted images",
    )
    parser.add_argument(
        "--markitdown-command",
        default="markitdown",
        metavar="COMMAND",
        help="MarkItDown executable name or path",
    )
    parser.add_argument(
        "--marker-command",
        default="marker_single",
        metavar="COMMAND",
        help="Marker executable name or path",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace an existing Markdown output and colliding generated assets",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the route and dependency availability without converting",
    )
    return parser.parse_args(argv)


def default_output_path(input_path: Path) -> Path:
    if input_path.suffix.lower() in MARKDOWN_SUFFIXES:
        return input_path.with_name(f"{input_path.stem}.converted.md")
    return input_path.with_suffix(".md")


def marker_options_requested(args: argparse.Namespace) -> bool:
    return any(
        (
            args.force_ocr,
            args.strip_existing_ocr,
            args.page_range,
            args.use_llm,
            args.disable_image_extraction,
        )
    )


def choose_plan(input_path: Path, args: argparse.Namespace) -> ConversionPlan:
    suffix = input_path.suffix.lower()
    marker_options = marker_options_requested(args)

    if args.engine == "markitdown":
        if marker_options:
            raise ConversionError(
                "Marker-specific options cannot be combined with --engine markitdown"
            )
        return ConversionPlan("markitdown", "explicit engine override")

    if args.engine == "marker":
        if suffix not in MARKER_SUFFIXES:
            raise ConversionError(
                f"Marker does not advertise support for {suffix or 'extensionless files'}; "
                "use MarkItDown or convert the source to a supported format first"
            )
        return ConversionPlan(
            "marker", "explicit engine override", force_ocr=args.force_ocr
        )

    if marker_options:
        if suffix not in MARKER_SUFFIXES:
            raise ConversionError(
                f"Marker-specific options were requested for unsupported type "
                f"{suffix or '<none>'}"
            )
        return ConversionPlan(
            "marker", "Marker-specific option requested", force_ocr=args.force_ocr
        )

    if suffix in IMAGE_SUFFIXES:
        return ConversionPlan("marker", "image input requires OCR", force_ocr=True)

    if suffix == ".pdf":
        return ConversionPlan(
            "markitdown",
            "try lightweight embedded-text extraction before OCR",
            pdf_ocr_fallback=args.ocr_threshold > 0,
        )

    return ConversionPlan("markitdown", "text-bearing or general document input")


def find_executable(command: str) -> str:
    executable = shutil.which(command)
    if executable is None:
        raise ConversionError(
            f"Required executable not found: {command}. "
            "Run scripts/check_dependencies.py for installation guidance."
        )
    return executable


def run_process(command: list[str]) -> subprocess.CompletedProcess[str]:
    try:
        completed = subprocess.run(
            command,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except OSError as exc:
        raise ConversionError(f"Could not start {command[0]}: {exc}") from exc

    if completed.returncode != 0:
        details = (completed.stderr or completed.stdout).strip()
        if len(details) > 4000:
            details = details[-4000:]
        raise ConversionError(
            f"{Path(command[0]).name} exited with code {completed.returncode}"
            + (f":\n{details}" if details else "")
        )
    return completed


def run_markitdown(input_path: Path, command: str) -> str:
    executable = find_executable(command)
    completed = run_process([executable, str(input_path)])
    if not completed.stdout.strip():
        raise ConversionError("MarkItDown produced empty output")
    return completed.stdout


def select_marker_markdown(stage: Path, input_path: Path) -> Path:
    candidates = list(stage.rglob("*.md"))
    exact = [candidate for candidate in candidates if candidate.stem == input_path.stem]
    if len(exact) == 1:
        return exact[0]
    if len(candidates) == 1:
        return candidates[0]
    if not candidates:
        raise ConversionError("Marker completed without producing a Markdown file")
    found = ", ".join(str(path.relative_to(stage)) for path in candidates)
    raise ConversionError(f"Marker produced multiple Markdown files: {found}")


def atomic_write_text(output_path: Path, content: str) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=output_path.parent,
            prefix=f".{output_path.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary:
            temporary.write(content)
            temporary_name = temporary.name
        os.replace(temporary_name, output_path)
        temporary_name = None
    finally:
        if temporary_name is not None:
            Path(temporary_name).unlink(missing_ok=True)


def copy_marker_result(
    generated_markdown: Path,
    output_path: Path,
    input_path: Path,
    overwrite: bool,
) -> int:
    source_root = generated_markdown.parent
    asset_sources = [
        path
        for path in source_root.rglob("*")
        if path.is_file()
        and path != generated_markdown
        and not path.name.endswith("_meta.json")
    ]
    asset_targets = [
        output_path.parent / source.relative_to(source_root) for source in asset_sources
    ]

    protected_input = input_path.resolve()
    collisions = []
    for target in [output_path, *asset_targets]:
        if target.resolve() == protected_input:
            raise ConversionError(f"Refusing to overwrite the source file: {target}")
        if target.exists() and not overwrite:
            collisions.append(target)
    if collisions:
        rendered = "\n".join(f"  - {path}" for path in collisions)
        raise ConversionError(
            "Output files already exist; choose another path or pass --overwrite:\n"
            f"{rendered}"
        )

    atomic_write_text(output_path, generated_markdown.read_text(encoding="utf-8"))
    for source, target in zip(asset_sources, asset_targets):
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    return len(asset_sources)


def run_marker(
    input_path: Path,
    output_path: Path,
    args: argparse.Namespace,
    force_ocr: bool,
) -> int:
    executable = find_executable(args.marker_command)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix=".marker-", dir=output_path.parent
    ) as temporary_dir:
        stage = Path(temporary_dir)
        command = [
            executable,
            str(input_path),
            "--output_dir",
            str(stage),
            "--output_format",
            "markdown",
        ]
        if force_ocr:
            command.append("--force_ocr")
        if args.strip_existing_ocr:
            command.append("--strip_existing_ocr")
        if args.page_range:
            command.extend(("--page_range", args.page_range))
        if args.use_llm:
            command.append("--use_llm")
        if args.disable_image_extraction:
            command.append("--disable_image_extraction")

        run_process(command)
        generated = select_marker_markdown(stage, input_path)
        return copy_marker_result(generated, output_path, input_path, args.overwrite)


def alphanumeric_count(markdown: str) -> int:
    return sum(character.isalnum() for character in markdown)


def print_dry_run(
    input_path: Path,
    output_path: Path,
    plan: ConversionPlan,
    args: argparse.Namespace,
) -> None:
    primary_command = (
        args.markitdown_command if plan.engine == "markitdown" else args.marker_command
    )
    primary_status = "found" if shutil.which(primary_command) else "missing"
    print(f"Input: {input_path}")
    print(f"Output: {output_path}")
    print(f"Primary engine: {plan.engine}")
    print(f"Reason: {plan.reason}")
    print(f"Executable: {primary_command} ({primary_status})")
    if plan.force_ocr:
        print("OCR: forced")
    if plan.pdf_ocr_fallback:
        fallback_status = "found" if shutil.which(args.marker_command) else "missing"
        print(
            "Fallback: Marker with forced OCR when MarkItDown output has fewer than "
            f"{args.ocr_threshold} alphanumeric characters "
            f"({args.marker_command}: {fallback_status})"
        )


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    input_path = args.input.expanduser().resolve()
    if not input_path.is_file():
        raise ConversionError(f"Input is not a local file: {input_path}")

    output_path = (
        args.output.expanduser().resolve()
        if args.output
        else default_output_path(input_path).resolve()
    )
    if output_path.suffix.lower() not in MARKDOWN_SUFFIXES:
        raise ConversionError("Output must end in .md or .markdown")
    if output_path == input_path:
        raise ConversionError("Output path must differ from the source file")
    if output_path.exists() and not args.overwrite and not args.dry_run:
        raise ConversionError(
            f"Output already exists: {output_path}. Pass --overwrite to replace it."
        )

    plan = choose_plan(input_path, args)
    if args.dry_run:
        print_dry_run(input_path, output_path, plan, args)
        return 0

    used_engine = plan.engine
    asset_count = 0
    if plan.engine == "marker":
        asset_count = run_marker(
            input_path, output_path, args, force_ocr=plan.force_ocr
        )
    else:
        markitdown_error: ConversionError | None = None
        try:
            markdown = run_markitdown(input_path, args.markitdown_command)
        except ConversionError as exc:
            markitdown_error = exc
            markdown = ""

        needs_fallback = plan.pdf_ocr_fallback and (
            markitdown_error is not None
            or alphanumeric_count(markdown) < args.ocr_threshold
        )
        if needs_fallback:
            reason = (
                str(markitdown_error)
                if markitdown_error
                else (
                    f"only {alphanumeric_count(markdown)} alphanumeric characters "
                    "were extracted"
                )
            )
            print(
                f"MarkItDown PDF extraction was insufficient ({reason}); "
                "retrying with Marker OCR.",
                file=sys.stderr,
            )
            asset_count = run_marker(input_path, output_path, args, force_ocr=True)
            used_engine = "marker"
        elif markitdown_error is not None:
            raise markitdown_error
        else:
            atomic_write_text(output_path, markdown)

    print(
        f"Converted {input_path} -> {output_path} "
        f"(engine={used_engine}, assets={asset_count})"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ConversionError as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(2)
