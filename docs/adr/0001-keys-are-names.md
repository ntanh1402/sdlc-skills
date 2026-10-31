# Keys are names, not sequence numbers

Several people draft changes to one Bundle at the same time, each on their own branch, so a sequence number handed out on one branch (`CR-3`, `ADR-004`, `REQ-checkout-5`) collides with the same number on another, and a Requirement number collision is caught by neither git nor `validate`. We therefore make every Key a descriptive name (`CR-sms-alerts`, `ADR-event-bus`, `TASK-orders-endpoint`, `REQ-checkout-pay-by-card`), which replaces the ID rules of the schema v2 spec section 6 and removes the need for a `next-id` command.

## Considered Options

- Allocate numbers locally and detect collisions at merge, then renumber: needs a new validate rule, a renumber step after approval, and still fails silently for Requirements until that rule exists.
- Reserve numbers centrally by pushing a reservation to the default branch: needs network and push rights for every draft and leaves junk commits behind rejected drafts.

## Consequences

- Indexes of ChangeRequests and decisions sort alphabetically; order in time is read from logs and git history.
- A Key never changes after it is merged, even when its text drifts from its name; a `rename` command exists for Draft branches only.
