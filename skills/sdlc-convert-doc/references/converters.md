# Converter reference

The skill pins the converter versions verified on 2026-07-14:

- `markitdown[all]==0.1.6`
- `marker-pdf==1.10.2` or `marker-pdf[full]==1.10.2`

Keep these exact pins when installing. Do not replace them with unversioned packages or
upgrade flags unless the skill is deliberately reviewed and updated for a newer release.

## MarkItDown

[Microsoft MarkItDown](https://github.com/microsoft/markitdown) is the default for
documents with extractable text. It preserves headings, lists, tables, and links while
remaining lightweight. Its official CLI is:

```bash
markitdown INPUT -o OUTPUT.md
```

Install Python 3.10+ and all optional format handlers in an isolated environment:

```bash
python -m pip install 'markitdown[all]==0.1.6'
```

MarkItDown supports PDF, Word, PowerPoint, Excel, images, audio, HTML, CSV, JSON,
XML, ZIP, EPUB, and additional formats. Optional extras can narrow the installation,
for example `markitdown[pdf,docx,pptx]==0.1.6`.

Treat paths as security-sensitive. MarkItDown performs I/O with the current process's
permissions; accept only intended local files and avoid permissive URI conversion for
untrusted input.

## Marker

[Datalab Marker](https://github.com/datalab-to/marker) is the OCR and layout engine.
Use it for images, scanned/image-only PDFs, garbled embedded text, equations, complex
tables, forms, and difficult reading order.

Install PDF and image support:

```bash
python -m pip install 'marker-pdf==1.10.2'
```

Install additional DOCX, PPTX, XLSX, HTML, and EPUB dependencies only when Marker
must process those formats:

```bash
python -m pip install 'marker-pdf[full]==1.10.2'
```

The official single-file CLI is:

```bash
marker_single INPUT --output_dir OUTPUT_DIR --output_format markdown
```

Useful options include `--force_ocr`, `--strip_existing_ocr`, `--page_range`,
`--disable_image_extraction`, and `--use_llm`. Marker downloads models and uses
PyTorch; expect greater startup time, disk use, memory use, and CPU/GPU demand than
MarkItDown.

Review Marker's current repository license before commercial or redistributed use.
Its README states that the code and model weights have different terms and describes
commercial-use thresholds. Do not infer that installing the package grants broader
rights.

## Routing behavior in the bundled script

- Route common images directly to Marker with forced OCR.
- Route PDFs to MarkItDown first. Retry with Marker and forced OCR when conversion
  fails or yields fewer than `--ocr-threshold` alphanumeric characters.
- Route other file types to MarkItDown unless Marker is explicitly selected.
- Route directly to Marker when a Marker-specific option is requested.
- Preserve Marker image assets beside the requested Markdown output and discard its
  auxiliary metadata JSON.

The sparse-text threshold is only a heuristic. Inspect every important conversion and
explicitly select Marker when the PDF has complex layout despite containing text.
