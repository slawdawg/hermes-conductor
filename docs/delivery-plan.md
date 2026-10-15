# Hermes Conductor Delivery Plan

**Status:** active

**Objective:** deliver Hermes Conductor as a public, upstream-compatible Hermes plugin that provides configurable, governed development and review workflows without a private Hermes core fork.

This is the authoritative implementation plan. It replaces the earlier plan to solve the project through a broad private refactor of `kanban_db.py` and `kanban_db_dispatch.py`.

## Operating decisions

1. **Plugin first.** Use documented plugin APIs, external Kanban worker lanes, commands, hooks, middleware, task comments/attachments, and plugin-owned durable state.
2. **No private imports or runtime patching.** Do not import `hermes_cli` private modules, modify internal tables, monkey-patch core functions, or couple to undocumented behavior.
3. **Hermes owns Kanban truth.** Hermes task status, dependency state, workspaces, and ordinary worker accounting remain canonical.
4. **Conductor owns policy truth.** Candidate identities, review receipts, policy releases, and audit data live in task artifacts/comments and a plugin-owned sidecar store.
5. **Core change is exceptional.** Only propose an upstream change if a tested requirement cannot be enforced before claim/spawn through a documented seam. The proposal must be generic, minimal, and independently useful.
6. **Review sequence.** Codex reviews every exact candidate before Claude performs a final independent review. Claude is never used for exploratory diagnosis.
7. **No production cutover by implication.** Each phase has an explicit evidence gate; production activation needs a separate approval.

## Success criteria

Conductor is complete when it can run a real task through configured development, Codex pre-review, and Claude final-review lanes on a clean supported Hermes release; bind all evidence to the same candidate identity; recover safely from expected runner failures; remain installable through the plugin catalog; and disable cleanly without corrupting ordinary Hermes tasks.

## Phase 0 — Preservation and requirements ledger

### Work

- Preserve the existing core-fork candidate as a hash-verified archival checkpoint; do not discard it.
- Export a behavior ledger from that candidate: each intended behavior, why it exists, existing regression evidence, its required enforcement point, and its target Conductor component.
- Classify every behavior as **plugin/lane**, **plugin policy**, **observer/diagnostic**, or **possible upstream primitive**.
- Record decisions and explicitly mark behavior that is intentionally out of scope for the first release.

### Exit gate

- Candidate archive verifies by SHA-256.
- No feature is silently dropped; every item has an owner/category/disposition.
- A clean upstream Hermes checkout is selected as the proof-of-concept target.

## Phase 1 — Supported-boundary proof of concept

### Work

- Implement a plugin configuration loader with schema validation, safe defaults, versioned migrations, and redacted diagnostics.
- Register one **external Kanban worker lane** through only documented APIs.
- Implement a minimal lane wrapper that receives the task/workspace/board contract, writes a structured receipt, and returns a PID when applicable.
- Add operator commands: status, validate-config, and verify-evidence.
- Prove installation, enablement, and removal against a clean supported Hermes release.

### Exit gate

- `hermes plugins doctor` and `hermes plugins validate --install-deps` pass.
- One real task completes through the external lane without private imports or core modifications.
- Disabling the plugin leaves the task board readable and ordinary Hermes operation intact.

## Phase 2 — Policy engine and evidence chain

### Work

- Build a sidecar store keyed by board/task/run identity using plugin-supported durable storage.
- Implement deterministic candidate identity: repository base, changed-file manifest, content hashes, selected test receipt, configuration revision, and wrapper version.
- Build immutable review packets and attach/export receipts without embedding credentials.
- Add explicit operator release/override records with rationale and identity binding.
- Implement policy states: draft, development-ready, pre-review-ready, final-review-ready, held, released, completed.

### Exit gate

- Rebuilding evidence produces the same identity for identical inputs.
- Any source/configuration/evidence mismatch blocks progression.
- A retained artifact and sidecar record can reconstruct the policy decision.

## Phase 3 — Configurable development and review lanes

### Work

- Implement named configuration profiles for development, Codex pre-review, and Claude final review.
- Support provider/model selection, prompt templates, read-only/write mode, timeouts, retry budgets, workspace policy, test commands, evidence retention, and notifications.
- Resolve profiles through allow-listed configuration only; task data cannot inject a model, command, path, or secret.
- Implement gate ordering: required Codex PASS bound to exact candidate before Claude can launch.
- Keep provider authentication host-owned; never persist secrets in Conductor state or packet artifacts.

### Exit gate

- A user can change models/providers and operational preferences entirely through validated configuration.
- Invalid, unknown, or insecure profile values fail closed before a runner starts.
- Codex-pre-review and Claude-final-review workflows are independently reproducible from evidence.

## Phase 4 — Recovery, holds, and operational controls

### Work

- Define wrapper exit taxonomy: success, policy failure, ordinary failure, timeout, cancellation, unknown/ambiguous exit.
- Implement idempotent receipt writes and restart-safe sidecar updates.
- Require an explicit hold for ambiguous exit, identity drift, unavailable required reviewer, or incomplete packet.
- Add operator commands to inspect, verify, release, and export a hold; all releases create auditable records.
- Implement configurable notifications, owner-action filtering, quiet hours, retention, and redaction.

### Exit gate

- Kill/restart/timeout simulations never create a false review PASS or automatic unsafe retry.
- Recovery preserves the original candidate identity and lane provenance.
- Operator controls work without direct database edits.

## Phase 5 — Compatibility, security, and regression verification

### Work

- Test against the declared Hermes compatibility floor and current stable release in clean isolated environments.
- Add contract tests for all documented extension surfaces used by Conductor.
- Add unit, integration, and end-to-end tests for happy path, configuration rejection, evidence mismatch, stale/unknown runner, review failure, and plugin disable/uninstall.
- Run static/security checks for private-core imports, forbidden monkey-patches, secret leakage, unsafe shell interpolation, committed bytecode, and undeclared dependencies.
- Require Codex review of the exact candidate before any Claude final review.

### Exit gate

- Supported-version matrix is green.
- All releases are source-only, reproducible, and free of undisclosed privileged behavior.
- Codex PASSes the exact release candidate; Claude independently PASSes the frozen review packet.

## Phase 6 — Pilot, migration, and cutover readiness

### Work

- Run a non-production pilot with representative development/review tasks.
- Compare Conductor behavior to the preserved core-fork behavior ledger; document deltas and user-visible tradeoffs.
- Provide configuration migration examples and a rollback/uninstall guide.
- Confirm ordinary Hermes can continue managing existing tasks when Conductor is disabled.
- Decide whether any remaining gap warrants a narrowly scoped upstream API proposal.

### Exit gate

- Pilot evidence meets the success criteria with no unresolved safety defect.
- Any fork-only behavior is either reproduced, consciously deferred, or proposed upstream with a concrete transaction-boundary justification.
- User explicitly approves production activation.

## Phase 7 — Catalog publication and maintenance

### Work

- Complete `docs/catalog-readiness.md` for the exact release commit.
- Publish a source-only tagged release and prepare an exact-SHA catalog entry.
- Open the reviewed catalog PR with complete capabilities, dependencies, risk disclosures, compatibility range, and maintainer information.
- Establish release policy: every update gets a new commit pin, changelog, validation run, Codex pre-review, and final independent review when release-risk warrants it.

### Exit gate

- Catalog entry is merged or the repository remains installable by pinned commit with the catalog checklist accurately reflecting its status.
- No automatic update channel or unreviewed mutable reference is used.

## Configuration contract

Users may customize: provider/model profile, prompt templates, review stages, timeout/retry values, workspace policies, test commands, notification destinations, quiet hours, evidence retention, and allowed lane roles.

The following remain invariant: exact-candidate evidence binding; auditable overrides; credential redaction; explicit holds for ambiguous results; no final review before required pre-review; and no arbitrary task-provided shell/model/provider configuration.

## Decision gate for an upstream change

A core change may be proposed only after a clean-upstream proof demonstrates a specific failure that cannot be addressed by an external lane, pre-spawn wrapper, plugin command, hook, middleware, or compensation workflow. The proposal must identify the exact race/transaction boundary, contain no organization-specific policy, add a public documented seam, and be independently tested upstream.

## Tracking and review cadence

- Keep this plan versioned in the repository.
- Track implementation work in linked GitHub issues, each mapped to a phase and an exit criterion.
- Do not start a later phase while its predecessor has an unresolved safety or compatibility failure.
- Maintain a release decision record with candidate hash, test receipts, Codex verdict, Claude verdict, and explicit activation authorization.
