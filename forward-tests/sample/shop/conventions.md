---
type: Convention
title: Shop engineering conventions
description: Rules every shop repository follows for code, review, tests, and finishing work.
generated: { by: human:sample-author, at: 2026-10-01T09:00:00Z }
verified: { by: human:sample-author, at: 2026-10-01T09:00:00Z }
---

# Shop engineering conventions

# Coding standards

* A service writes only the tables it lists under `# Writes`. Reading another
  service's table is allowed only when the wiki lists it under `# Reads`.
* Anything optional to a purchase happens after an event, never inside the
  checkout request.
* An endpoint that creates money movement or an order accepts a client
  idempotency token and returns the first result on a retry.
* Card data never reaches a shop service; only provider tokens do.

# Branching and review

* One Task is one branch and one pull request. Branches are named
  `feat/<area>-<slug>` or `fix/<area>-<slug>`.
* The pull request title carries the tracker key of its Task.
* A pull request needs one approving review and a passing pipeline.

# Testing policy

* Unit tests live beside the code they test.
* Integration tests cover each datastore, channel, and external boundary a
  service touches.
* End-to-end tests live in the shared `e2e-tests` repository.
* The name of a runnable test contains the key of the TestCase it implements.

# Definition of done

* The pull request is merged and the pipeline is passing.
* The Task is `Done` here and in the tracker.
* Every Design concept the Task covered has its pending entry removed and its
  status set to `Active`, unless other unfinished work still covers it.
