# Hermes Conductor v0.1 Product and Technical Specification

**Status:** proposed implementation specification

**Scope:** source-only, upstream-compatible Hermes plugin proof of concept and first governed workflow release.

## 1. Purpose

Hermes Conductor provides configurable, evidence-backed development and review lanes for Hermes without modifying Hermes core. It turns a task into a governed delivery flow:

`development → evidence verification → Codex pre-review → optional Claude final review → complete or explicit hold`

Hermes remains the canonical owner of task lifecycle and workspaces. Conductor owns workflow policy, configuration, receipts, and operator-facing controls.

## 2. Goals

1. Install as a standalone public Hermes plugin using documented plugin APIs only.
2. Allow users to select approved development and review provider/model profiles through configuration.
3. Support one external development lane and one read-only Codex pre-review lane.
4. Bind each review receipt to an exact candidate identity.
5. Prevent an enabled final-review lane from starting until required Codex evidence passes for that exact identity.
6. Make status, failure causes, holds, and release operations understandable without database access.
7. Preserve ordinary Hermes task usability when Conductor is disabled or uninstalled.
8. Be ready for catalog submission once implementation, automated verification, and disclosures are complete.

## 3. Non-goals for v0.1

- Replacing Hermes scheduler, database, task status model, worker reaper, or workspace implementation.
- Importing private `hermes_cli` APIs or monkey-patching Hermes internals.
- Atomic modification of Hermes claim transactions.
- Multi-repository release coordination.
- Dashboard UI, hosted service, automatic telemetry, or cloud evidence storage.
- Arbitrary task-provided shell commands, model IDs, provider IDs, paths, or credentials.
- Automatic release of ambiguous/unknown runner outcomes.

## 4. Personas

### Solo developer

Wants a simple default: an implementation runner plus Codex review, with one local config file and no external service.

### Team/release owner

Wants required Codex pre-review followed by a separate final-review profile, immutable evidence, and an explicit hold for unusual failure conditions.

### Advanced operator

Wants to use local or hosted providers, custom timeouts and notifications, and strict configuration validation without forking Hermes.

## 5. User experience

### 5.1 Setup

`/conductor-setup` asks for a preset and named configured profiles. It writes only a profile-scoped configuration file and reports its location. It never asks for or writes credentials; provider authentication remains Hermes-owned.

Presets:

| Preset | Development | Codex pre-review | Final review |
|---|---|---|---|
| `simple` | required | disabled | disabled |
| `governed` | required | required | disabled |
| `team-release` | required | required | required when enabled on task policy |

### 5.2 Essential commands

| Command | Result |
|---|---|
| `/conductor-status [task]` | Summarizes configuration revision, policy state, candidate identity, receipts, active hold, and next safe action. |
| `/conductor-validate-config` | Validates schema, profiles, compatibility, path safety, and unavailable provider references without launching a runner. |
| `/conductor-dry-run <task>` | Shows the exact lane/profile that would be used, gates, expected receipts, and blocked reason. No runner starts. |
| `/conductor-verify-evidence <task>` | Recomputes and verifies receipt/payload identity binding. |
| `/conductor-release <task> --reason <text>` | Records an explicit, auditable operator release for an eligible hold. |
| `/conductor-export-evidence <task>` | Creates a redacted, portable evidence bundle. |

### 5.3 User-visible failure rules

Every failure/hold response includes: policy state, task identity, candidate hash, condition that failed, receipt path or missing record, and an exact safe next action. It must never recommend direct SQLite edits.

## 6. Configuration

### 6.1 Location and precedence

1. Plugin defaults, bundled and immutable.
2. Optional profile-scoped policy YAML selected through plugin configuration `config_path`.
3. No task-body or environment-variable override of provider, model, command, or workspace path.

User-owned secret configuration remains in Hermes/provider mechanisms and is not read or exported by Conductor.

### 6.2 Configuration schema

```yaml
version: 1
preset: governed
profiles:
  development:
    lane: conductor-development
    provider: codex
    model: <configured-model-name>
    max_runtime_minutes: 120
    workspace_mode: write
    retry: { max_attempts: 1, manual_hold_on_uncertain_exit: true }
  pre_review:
    lane: conductor-codex-pre-review
    provider: codex
    model: <configured-model-name>
    workspace_mode: read_only
    max_runtime_minutes: 60
  final_review:
    lane: conductor-final-review
    provider: claude
    model: <configured-model-name>
    workspace_mode: read_only
    max_runtime_minutes: 90
gates:
  require_candidate_hash_match: true
  require_pre_review_before_final: true
  final_review_enabled: false
evidence:
  hash_algorithm: sha256
  retain_days: 90
notifications:
  owner_actions_only: true
  quiet_hours: { timezone: America/Chicago, start: '22:00', end: '08:00' }
```

### 6.3 Validation requirements

- Reject unknown schema versions, unknown presets, unknown profile references, unknown keys in strict mode, invalid timeout/retry ranges, unsafe path values, and unsupported workspace modes.
- Profile names use a constrained identifier grammar; no arbitrary executable or shell fragments are accepted.
- Provider/model values must reference profiles available through Hermes configuration; missing/unavailable profiles block startup or dry-run.
- The normalized configuration is canonicalized and hashed. The hash is recorded in every receipt.

### 6.4 Invariants users cannot disable

- Candidate identity matching for dependent receipts.
- Auditable overrides/releases.
- Credential redaction.
- Manual hold on unknown/ambiguous runner exit.
- No final review before required pre-review evidence passes.
- No task-supplied command/provider/model/path injection.

## 7. Architecture

```
Hermes plugin runtime
 ├─ Conductor command handlers
 ├─ Config loader / normalizer
 ├─ Policy engine
 ├─ External worker lane adapters
 │   └─ constrained runner wrapper process
 ├─ Evidence builder / verifier
 ├─ Sidecar state store
 └─ Hooks / observers for receipt reconciliation and diagnostics

Hermes Kanban
 ├─ canonical task status / dependencies / workspaces
 ├─ plugin external-lane dispatch contract
 └─ task comments / attachments for visible evidence
```

### 7.1 Supported integration contract

Conductor may use only documented plugin registration, configuration/state facilities, task-facing APIs, external worker lanes, commands, hooks, middleware, and storage interfaces. Any attempt to use a private Hermes import is a failing static check.

### 7.2 External worker lanes

v0.1 registers:

- `conductor-development`
- `conductor-codex-pre-review`
- `conductor-final-review` (implemented but disabled unless the configuration enables it)

Each lane adapter receives the documented task/workspace/board contract, constructs a validated wrapper request, starts a configured runner, writes receipts, and returns the PID when a persistent child exists. A runner wrapper is the hard boundary for workspace mode and process environment; in-process hooks are not the sole security boundary.

### 7.3 Sidecar store

The sidecar store uses plugin-owned durable storage. It stores no raw credentials or task prompt body by default.

Minimum logical records:

- `policy_run`: board ID, task ID, Hermes run correlation, policy state, config hash, timestamps.
- `candidate`: base revision, changed-file manifest hash, aggregate candidate hash, test receipt hash.
- `receipt`: receipt kind, producer lane/profile, candidate hash, config hash, verdict, timestamp, artifact reference, content hash.
- `hold`: reason code, human-readable explanation, evidence reference, release eligibility, release record.
- `release`: operator identity available from command context, reason, timestamp, prior hold hash.

State writes must be idempotent under a stable policy-run/candidate/receipt key.

## 8. Policy state machine

| State | Entry condition | Permitted next state |
|---|---|---|
| `unmanaged` | Task has no Conductor policy context. | `development_ready` |
| `development_ready` | Config and task policy validate. | `development_running`, `held` |
| `development_running` | Development lane wrapper launched. | `evidence_pending`, `held` |
| `evidence_pending` | Development finished; candidate/evidence being built. | `pre_review_ready`, `held` |
| `pre_review_ready` | Candidate identity and required development evidence verify. | `pre_review_running`, `held` |
| `pre_review_running` | Codex lane wrapper launched. | `final_review_ready`, `held` |
| `final_review_ready` | Required Codex PASS matches candidate/config hash. | `final_review_running`, `completed`, `held` |
| `final_review_running` | Final-review wrapper launched. | `completed`, `held` |
| `held` | Ambiguous exit, invalid evidence, required reviewer unavailable, or policy failure. | prior safe state through audited release, `completed` only with approved policy evidence |
| `completed` | Required configured gates passed. | terminal |

If the final-review gate is disabled, `pre_review_running → completed` after a candidate-bound Codex PASS.

## 9. Candidate identity and evidence

### 9.1 Candidate identity input

A candidate identity contains:

- declared repository base revision;
- sorted changed-file paths and SHA-256 values;
- normalized configuration hash;
- selected test-gate command/result receipt hash;
- Conductor version and wrapper version.

The aggregate identity uses a documented canonical JSON encoding and SHA-256. All receipt payloads include the aggregate identity and configuration hash.

### 9.2 Receipt format

Receipts are JSON documents with schema version, producer, profile, timestamps, candidate identity, configuration hash, verdict, summarized runner exit, artifact paths, and content hash. Logs may be referenced, but secrets and unredacted provider material must not be copied into receipts.

### 9.3 Review gate

A final-review launch is denied unless:

1. the configuration enables final review;
2. a Codex receipt exists;
3. its verdict is `pass`;
4. its candidate hash and config hash match the current verified identity; and
5. no unreleased hold exists.

## 10. Runner safety and recovery

### 10.1 Wrapper input contract

The wrapper receives only normalized configuration, selected profile identifier, declared workspace path, task identity, policy-run ID, and artifact output path. It must not receive raw provider credentials through Conductor.

### 10.2 Exit taxonomy

- `success`: required receipt written and verifiable.
- `failure`: runner completed with a known non-success result; policy blocks subsequent gate.
- `timeout`: runtime exceeded configured limit; task enters hold.
- `cancelled`: explicit cancellation; task enters hold or returns to a safe earlier state according to policy.
- `unknown`: missing/corrupt exit/receipt, lost process, or inconsistent state; task enters manual hold.

No exit state creates a PASS without a complete, hash-valid receipt.

### 10.3 Idempotency

Rerunning a wrapper for the same policy run/candidate/profile must either reuse an identical valid receipt or create a separately timestamped attempt record. It must never overwrite a prior PASS with an unrelated candidate result.

## 11. Security and privacy

- No telemetry in v0.1.
- No self-updater or mutable remote code loader.
- No credential collection; rely on Hermes/provider-owned authentication.
- No recursive collection of home directories, browser profiles, shell history, environment files, or keychains.
- Workspace mode is enforced by the wrapper contract and approved runner invocation, not merely documentation.
- Use safe argument arrays, not shell interpolation, for runner execution.
- Redact configured secret-like values from diagnostic and evidence exports.
- Source-only releases; reject committed bytecode/binaries/untracked generated artifacts.

## 12. Testing and review requirements

### 12.1 Automated tests

- Configuration parsing, normalization, validation, migrations, and redaction.
- Candidate identity determinism and evidence tamper detection.
- State-machine transition coverage including every hold reason.
- Wrapper request construction and safe argument handling.
- Development/pre-review/final-review flow with fake providers.
- Plugin installation, enablement, disablement, and removal against clean supported Hermes versions.
- Regression tests asserting no private Hermes imports or runtime rebinding.
- Catalog validator and plugin doctor on the exact release candidate.

### 12.2 Review gates

- Codex reviews the exact implementation candidate before Claude is asked to review.
- Claude final review receives a frozen, candidate-bound packet; incomplete/terminated review never counts as approval.
- Every reported defect receives a regression test or documented rationale before the next review cycle.

## 13. Release and catalog requirements

A release candidate requires:

1. source-only clean repository;
2. complete README behavior/security disclosures;
3. versioned manifest and compatibility range;
4. green supported-version test matrix;
5. passed plugin doctor and catalog validator;
6. exact candidate hash and evidence bundle;
7. Codex PASS, then valid independent Claude final PASS where required;
8. an exact-SHA catalog entry submitted through the reviewed Hermes catalog process.

## 14. Acceptance scenarios

1. **Governed happy path:** user configures development and Codex profiles, runs a task, obtains candidate-bound Codex PASS, and completes without a final reviewer enabled.
2. **Team-release path:** same workflow with final review enabled; Conductor refuses final-review launch before Codex receipt verifies, then accepts matching final PASS.
3. **Configuration error:** invalid model/profile/timeout causes `/conductor-validate-config` to fail without spawning a process.
4. **Evidence mismatch:** source or config changes after Codex PASS; final review is blocked with an actionable mismatch hold.
5. **Unknown runner exit:** wrapper PID/receipt is missing; Conductor creates a hold, never treats it as a retry/PASS, and `/conductor-release` records an explicit resolution.
6. **Plugin disabled:** existing Hermes task records remain readable and manageable; Conductor sidecar state can be exported.

## 15. Open decision: upstream primitive

After Phase 1 through Phase 5, evaluate whether the lack of an atomic pre-claim/pre-dispatch veto leaves an unacceptable proven race. If not, ship without core changes. If yes, create a separate generic upstream proposal that identifies the exact boundary and test case; do not add a private scheduler fork.
