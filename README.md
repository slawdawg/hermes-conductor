# Hermes Conductor

**Governed, configurable multi-agent delivery for [Hermes Agent](https://github.com/NousResearch/hermes-agent).**

Hermes Conductor is an upstream-compatible plugin for teams and individuals who want explicit development, pre-review, and final-review lanes without maintaining a private Hermes fork.

It is built around Hermes' documented plugin APIs and external Kanban worker lanes. Hermes remains authoritative for task state and workspaces; Conductor owns policy, evidence, review sequencing, and configurable runner preferences.

> Status: design and compatibility proof-of-concept. Not yet ready for production use.

## What it will provide

- Configurable development, pre-review, and final-review lanes.
- Model/provider profiles selected by configuration rather than hard-coded policy.
- Evidence packets bound to an exact candidate identity.
- A required pre-review gate before final independent review.
- Operator-visible holds for uncertain runner exits.
- Task attachments/comments plus a portable sidecar evidence store.
- Notifications, quiet hours, retention, and retry preferences.

## What it deliberately does not do

- Patch or import Hermes private internals.
- Store credentials in task prompts, configuration exports, or evidence packets.
- Replace Hermes' canonical Kanban lifecycle state.
- Pretend that post-commit observers are atomic scheduler enforcement.

## Configuration philosophy

Choose your own providers, models, timeouts, notifications, and review sequence. Conductor keeps a few invariants non-configurable: evidence must match the reviewed candidate, credentials are redacted, ambiguous runner exits create an explicit hold, and overrides are auditable.

See [`docs/architecture.md`](docs/architecture.md) and [`examples/config.yaml`](examples/config.yaml).

## Compatibility

Conductor will target clean, released Hermes versions and validate its integration boundary in CI. If Hermes lacks a necessary atomic extension seam, Conductor will propose a small generic upstream API rather than maintain a scheduler fork.

## License

Apache-2.0
