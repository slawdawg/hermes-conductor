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

See [`docs/architecture.md`](docs/architecture.md), the versioned [`docs/delivery-plan.md`](docs/delivery-plan.md), the implementation [`docs/spec-v0.1.md`](docs/spec-v0.1.md), and [`examples/config.yaml`](examples/config.yaml).

## Compatibility

Conductor will target clean, released Hermes versions and validate its integration boundary in CI. The initial compatibility floor is Hermes `0.21.6`. If Hermes lacks a necessary atomic extension seam, Conductor will propose a small generic upstream API rather than maintain a scheduler fork.

## Catalog and security disclosures

Hermes Conductor is designed for catalog submission, but it will not be submitted until its documented external-lane proof of concept is complete and validated at a pinned release commit.

**Current `0.1.0` behavior:** it registers only the `/conductor-status` command. It makes no network calls, runs no shell commands, starts no background process, reads no credentials, and stores no telemetry.

**Planned operational behavior:** configured lane wrappers may launch user-selected local review/development runners. Before that capability is released, this README will disclose every network endpoint, command execution mode, data path, background process, credential route, and retention behavior. Telemetry will remain opt-in.

The plugin has no self-updater. Catalog installs will be exact commit pins, and updates will be delivered only through the Hermes catalog SHA-bump process.

See [`docs/catalog-readiness.md`](docs/catalog-readiness.md) for the maintained admission checklist.

## License

Apache-2.0
