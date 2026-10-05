# sdlc-convert-doc

Turn a PDF, scan, Word, PowerPoint, Excel, HTML or similar file into Markdown,
so the other skills can read it. [Back to the user guide](user-guide.md).

## At a glance

| | |
|---|---|
| **Who** | Anyone who has a brief, spec or architecture document that is not plain text |
| **Use when** | A source for `sdlc-write-spec` or `sdlc-import` is a PDF, scan, image, Word, PowerPoint, Excel, HTML, EPUB, email or archive |
| **Needs first** | The file on your disk, and the converters installed (the skill checks) |
| **Say** | "Convert brief.pdf to Markdown" |
| **You get** | A Markdown file next to the original, or where you say. The original is never changed |
| **Next** | Check the Markdown against the source, then run `sdlc-write-spec` or `sdlc-import` on it |

This skill does not use the wiki. It has no gates and no draft.

## What the skill does

1. Confirms the input is a local file and picks a separate output path ending
   in `.md`.
2. Checks that the converters are installed at the right versions.
3. Picks the engine:
   - **MarkItDown** for Word, PowerPoint, Excel, HTML, EPUB, email, CSV, JSON,
     XML, ZIP and PDFs that have real text. It is fast.
   - **Marker** for images, scanned or garbled PDFs, and PDFs with heavy
     layout, equations or complex tables. It does OCR and is slower.
4. Converts, then reads the Markdown it produced: headings, reading order,
   tables, equations, image links, missing text and OCR damage.
5. Reports what it found.

## What you do

- Say where the file is and, if you care, where the Markdown goes.
- **Check the result against the source.** Conversion is extraction, not proof.
  Look at the numbers, names, dates, tables and formulas that matter, because
  these are what the spec or import will rely on.

## Scenarios

| What happens | What the skill does | What you do |
|---|---|---|
| **A Word, PowerPoint or Excel file** | Converts with MarkItDown | Check tables and slide order |
| **A PDF with selectable text** | Tries MarkItDown first so no heavy model loads | Check the result |
| **A PDF that gives almost no text** (scanned or image-only) | Retries with Marker and forced OCR | Check names, dates and numbers carefully, because OCR makes mistakes |
| **The result is still poor** | Offers to rerun with Marker and OCR forced, overwriting the output | Approve the overwrite |
| **An image** (PNG, JPEG, TIFF, BMP, GIF, WebP) | Uses Marker, which does OCR and layout recovery | Check the text |
| **Equations or complex tables** | Uses Marker for stronger layout and math handling | Check the formulas against the source |
| **A converter is missing, or its version is wrong** | The preflight fails and the skill tells you what is missing. It does not upgrade the converters on its own | Install the pinned versions (see the skill's `references/converters.md`), then run again |
| **The output file already exists** | Refuses to overwrite | Say yes to replace it, or pick another name |
| **You are not sure which engine fits** | Previews the routing decision first (a dry run) | Confirm |
| **A web address instead of a file** | Refuses. Only local files are accepted | Download the file first |
| **The document is confidential** and the skill could send it to a model service (`--use-llm`) | Does not enable that without asking which service is configured and whether the document may go there | Decide whether the document may leave your machine |
| **Only some pages matter** | Can convert a page range | Say which pages |

## Not this skill

| Request | Use |
|---|---|
| Turning the Markdown into requirements | [sdlc-write-spec](sdlc-write-spec.md) |
| Recording the document in the wiki as an as-built source | [sdlc-import](sdlc-import.md) |
