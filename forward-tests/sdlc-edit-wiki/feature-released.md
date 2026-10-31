# A Feature marked released

## Wiki
`forward-tests/seed.sh <dir>`; then in `wiki/shop/features/FEAT-catalog/overview.md` set `status: InDev` and remove the `releasedAt` line, commit and push (an `InDev` Feature whose Tasks are all `Done`).

## Request
"FEAT-catalog shipped today, mark it released"

## Answers
- Asked for the time: "today, midnight"
- Approve each gate

## Expected
- Reads the Feature's Tasks: both are `Done`
- The stop shows `status InDev → Released` and `releasedAt`
- Draft `edit-FEAT-catalog`; the Feature has `status: Released` and `releasedAt`; a `**Released**` entry in its `log.md`
- `validate` ok, and the warning `pending.feature-built` is gone
