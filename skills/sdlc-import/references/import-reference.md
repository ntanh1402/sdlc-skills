# Importing a reference

One run keeps one piece of material for others to read while they work, as a
Reference: a page that explains a domain term, a vendor's documentation, a
document that is not a PRD, an architecture document or a test plan, or a
code location to follow as an example. It writes nothing else: no Design
file, Feature or decision. Read `reference.md` in `.wiki-llm/schema/` first.

The question "is what it describes built and running today?" does not apply:
a Reference is context, not a record of the system.

## 1. What to write

`references/REF-<name>/` with:

| File | Content |
|---|---|
| `overview.md` | `status: Active`, the summary, `# Contents`, and `resource` when the material lives outside the wiki |
| content files | The material as Markdown, with the images it links, and the original file the Markdown was converted from |
| `log.md` | One `**Import**` entry |

Rules:

- **A page or a document** is copied whole into a content file named after
  it. A PDF, Word or slide file is converted with `sdlc-convert-doc` first,
  and the original is kept beside the copy. A page on a site the person
  names is also `resource`.
- **A code location** is not copied. `resource` names it at a commit or a
  tag, never a branch:
  `https://github.com/acme/orders-service/blob/v1.4.0/src/orders/idempotency.ts`.
  `# Contents` is `None`, unless the person asks for short excerpts in a
  content file. The overview says what the code shows, what to follow and
  what not to copy, and `stale_after` is proposed, because code moves.
- **The key and the description** come from what the material is about, not
  from its file name: `REF-idempotency-key-handling`, "Code example of how
  the orders service makes a create request safe to repeat; read before
  building an endpoint that must not act twice."
- **Links to it.** Propose the concepts that should link it under
  `# References`, each with a note on what to take from it. They are written
  in the same draft, in the same group as the Reference.
- **Already in the wiki.** A Reference with the same `resource`, or with the
  key you would propose, is compared (`compare.md`): the new material is a
  difference the person decides.

## 2. What to ask

- What the material is for: the subject, and when someone should read it.
- For code: the commit or tag to pin, and what to follow and not to copy.
- Which concepts should link it.

## 3. Before the Design gate

Check by reading:

- the overview summarises the material and does not hold the whole of it;
- a code `resource` names a commit or a tag;
- the content files hold the whole material, and their links resolve;
- no secret or personal data was copied.
