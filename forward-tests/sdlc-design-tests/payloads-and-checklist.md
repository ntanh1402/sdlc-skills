# Payloads and checklist

## Wiki
`forward-tests/seed.sh <dir> --fixture order-notes-feature` (an `Approved` Feature whose design adds `EP-orders-note-put` and `EP-orders-note-get`).

## Request
"Design the integration tests for order notes"

## Answers
- Choose `integration` only, accepting the other gaps
- Confirm the other recommendations
- Approve each gate

## Expected
- Each `TC-*.md` has `# Test data` as a `No | Input | Value` table numbered 1, 2, 3, …
- Each step that calls `PUT` or `GET` on the notes endpoint says "Request: see Step <n>" and has a `### Step <n>` block with a `Request` (method, path, headers, body) and an `Expected response` (status, only the checked fields, then "Other fields are ignored."); the fields are those of the Endpoint files
- The suite's `overview.md` has `basedOn` with one entry `{ id: FEAT-order-notes, version: 1, at: <its versionDate> }`
- `tests/TS-order-notes-integration/checklist.csv` exists on the branch, written by `draft finish`: header `No,Title,Description,Covers,Purpose`, one row per case, highest risk first, `Covers` as keys joined by `; `
- The skill did not write `checklist.csv` or `index.md` itself
- `validate` ok
