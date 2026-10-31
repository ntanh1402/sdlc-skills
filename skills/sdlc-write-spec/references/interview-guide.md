# Requirements interview guide

This guide says what to ask about. How to ask (rounds, a recommendation with
each question, at least one round) is in `SKILL.md` section 2. Skip
what is already answered; do not turn the checklist into a questionnaire.

## Readiness

A Feature's intent is ready when each of these is known or recorded as an open
question, one line per PRD section:

- Summary: what changes for whom, why now, the owner and the priority.
- Problem and evidence: the problem, and what shows it is real.
- Goals and success metrics: a primary metric and a guardrail metric that
  must not get worse. A missing baseline or target is an open question; it
  does not block `ReqApproved`.
- Users and personas: the actors and what each needs. Who is excluded goes
  under out of scope.
- User flows: the trigger, plus the happy, alternate and failure flows.
- Business rules: the inputs, outputs, sensitive data, events, external
  parties and observable failure behaviour each Requirement needs.
- Requirements: functional, nonfunctional and constraint, each with a
  verification method; measurable quality targets when known.
- Release and rollout: phases, a feature flag, a migration or a deadline;
  ask only when the brief mentions one.
- Risks, assumptions and open questions.
- Out of scope.

A ChangeRequest's intent also needs:

- The confirmed target Feature, its current behaviour, the desired behaviour
  and the reason now.
- The rejected no-change option, and the behaviour that must not change.
- The Requirements added, changed and removed. A changed Requirement reuses
  the Feature's key; a removal is described, never written as a new positive
  Requirement.
- Compatibility, migration and rollback constraints, stated without choosing a
  technical solution.
- A confirmed `changeType` and an evidence-based `riskLevel`.

## Fast path

When a supplied brief or the conversation answers every readiness item, the
round is short: the Application, mode and target to confirm, the assumptions
you would make, the contradictions and missing verification you found, and
the wiki question. Add only decisions that change scope. Every gate still
applies: a complete brief is not an approval.

Stop asking when the remaining answers are predictable and every readiness
item is answered or recorded as an open question. Vague assent is not
approval. Surface hidden assumptions and the smallest useful scope, and say
what is not being done.

## Contradictions, and no one to ask

When the user's intent conflicts with the wiki, show both claims and their
paths, and ask whether the user is changing recorded behaviour or believes the
wiki is out of date. The first belongs in the spec. The second blocks writing
until the truth is settled.

When a blocking question remains and nobody can answer, return the open
decisions and write nothing.

## Change type and risk

Choose the primary `changeType` from evidence:

- `feature`: externally observable behaviour is added or changed.
- `bugfix`: behaviour violates an approved Requirement.
- `refactor`: internal structure changes, behaviour does not.
- `security`: confidentiality, integrity, authorization, abuse, audit or
  compliance control.
- `perf`: a measurable latency, throughput, resource or capacity outcome.

Ask when two types would route review differently; record secondary concerns
in the PRD.

Calibrate `riskLevel` without inventing facts:

- `critical`: plausible irreversible data loss, material security, compliance
  or safety impact, or an outage of a critical journey.
- `high`: crosses services, breaks compatibility, touches sensitive data, or is
  hard to roll back.
- `med`: bounded, known dependencies with a practical rollback.
- `low`: isolated and reversible, with a small regression surface.

An unknown owner, risk or verification stays an open question and blocks
`ReqApproved`.
