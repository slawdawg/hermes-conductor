# Architecture

## Boundary

Hermes Conductor is a separately versioned plugin. It relies only on documented Hermes plugin behavior:

- plugin configuration/state and commands;
- external Kanban worker lanes for runner ownership;
- hooks and middleware for observation and ordinary tool policy;
- task comments and attachments for visible evidence.

It never imports or monkey-patches private Hermes modules.

## Components

- **Policy engine:** validates a configuration profile and determines whether a lane may start.
- **Lane adapters:** documented external worker lanes for development, pre-review, and final review.
- **Runner wrappers:** invoke the configured provider/model with a constrained workspace/environment contract.
- **Evidence store:** records candidate hashes, test receipts, review verdicts, release records, and configuration revision.
- **Operator commands:** status, verify, release, and export functions.

## Configuration model

A user selects named provider/model profiles. Tasks reference lane roles, never arbitrary shell strings or credentials. Configuration is profile scoped, schema validated at startup, and its revision is captured in evidence.

Configurable: models/providers, prompts, timeouts, retry budgets, required review stages, notification routing/quiet hours, retention, test commands, and approved workspace policies.

Not configurable away: exact-candidate evidence binding, redaction, auditable overrides, and explicit handling of ambiguous runner exits.

## Compatibility posture

The proof-of-concept must run against a clean upstream Hermes checkout. A change that needs to be atomic with internal task claiming or default worker spawning is not implemented by an observer hook. If a real requirement remains, it becomes a narrowly scoped upstream API proposal with the policy itself remaining in Conductor.
