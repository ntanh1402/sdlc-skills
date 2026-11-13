# Payloads and checklist

## Wiki
`forward-tests/seed.sh <dir> --fixture order-notes-feature` (an `Approved` Feature whose design adds `EP-orders-note-put` and `EP-orders-note-get`).

## Request
"Design the Feature-level tests for order notes"

## Answers
- Choose `integration` cases only, accepting the other gaps
- Confirm the other recommendations
- Approve each gate

## Expected
- Each case has no `# Test data`; the data that must exist is in `# Preconditions` with concrete values
- Each step that calls the notes endpoint says "Call API `PUT /orders/{id}/note`" (or `GET`) with its values in the Action cell, never "see Step <n>" or "data <n>", and has a `### Step <n>` block with a `Request` (method, path, headers, body) and an `Expected response` (status, only the checked fields, then "Other fields are ignored."); the fields are those of the Endpoint files
- A step that checks the database names the table by its `tableName` (`orders`), never `TBL-orders`
- Each Expected result is one `<name>:` checkpoint per table or response with `- <field>: <value>` lines joined with `<br>` (`Response PUT /orders/{id}/note:<br>- status: 200`), and each Validation names the checked fields in bold
- `GENERAL/overview.md` has `basedOn: { version: 1, at: <its versionDate> }`; the suite's `overview.md` has none
- `tests/TS-order-notes/checklist.csv` exists on the branch, written by `draft finish`: header `No,Group,Title,Description,Category,Covers,Purpose`, one row per case, highest risk first, `No` the case id, `Group` `GENERAL`, `Covers` empty
- The skill did not write `checklist.csv` or `index.md` itself
- `validate` ok
