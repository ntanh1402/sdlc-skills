# Revise a designed draft

A draft Feature that is already designed is revised in place; its version
goes up and the design is reported as outdated.

## Wiki
The directory kept by `sdlc-design-arch/draft-feature.md`, after merging `wiki/arch-FEAT-gift-cards` into `main` and pushing `main`.

## Request
"Gift cards can also pay the shipping cost; add that"

## Answers
- Confirm the recommendations
- Approve each gate
- Status question: "keep it as a draft"

## Expected
- Mode: revise `FEAT-gift-cards` (it is `Draft`), not a ChangeRequest
- `version: 2`, `versionDate` today, `status: Draft`; `# Architecture` and `designBasedOn` (version 1) unchanged
- `validate` reports `basis.outdated` on `FEAT-gift-cards/overview.md` as a warning, and no error
- The summary lists the design under "For other skills" with `sdlc-design-arch`, and says `sdlc-edit-wiki` can record it as still current
- "Next" is `sdlc-design-arch` again for the new version
