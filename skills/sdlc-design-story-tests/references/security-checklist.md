# Security checklist

- Missing, expired and revoked authentication; session fixation.
- Horizontal and vertical authorization; tenant isolation.
- Injection, malformed payloads, unsafe deserialization, file and path abuse.
- Rate and abuse controls, replay, CSRF where relevant, leaked secrets or
  tokens.
- PII minimization, encryption, retention and deletion, audit evidence.
- External and webhook signature checks; failures at trust boundaries.

Write `security-validation` cases only when the user chooses them.
