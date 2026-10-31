# Show an endpoint

## Wiki
`forward-tests/seed.sh <dir>`.

## Request
"Show me EP-orders-create"

## Answers
- None scripted; improvise the most plausible short reply

## Expected
- The seven parts of the "show an endpoint or a consumer" recipe: summary, input, output with its status codes, validations, behavior, then the stored flowchart and sequence diagram unchanged, and `# Pending changes` when present
- The flowchart and the sequence diagram are the stored Mermaid blocks, not redrawn
- Nothing is written: `git status --short` is empty and no draft is started
- Asked for `SUB-order-created`, the input is the channel's payload linked from `# Consumes`, and the output is the side effects of `# Handler`
