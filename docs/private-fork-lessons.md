# Private-Fork Lessons and Migration Ledger

This document preserves the work, regressions, and operational lessons from the earlier core-fork candidate. The project is changing implementation boundary—not discarding its safety requirements.

The archived candidate checkpoint is the forensic source. Each item below must be carried into Conductor as a requirement, test, architectural constraint, or consciously documented non-equivalence.

## Carry-forward requirements

| Fork lesson / behavior | Why it was learned | Conductor target | Verification |
|---|---|---|---|
| Codex pre-review must complete before Claude final review begins. | Intermediate and final review must be independent; Claude is not an exploratory debugger. | Policy state machine and gate verifier. | Final lane dry-run and spawn deny without a matching Codex PASS. |
| Review evidence must bind to the exact candidate, not merely task ID or branch name. | Task state can change between review attempts. | Candidate identity, receipt schema, frozen review packet. | Change one file/config field after PASS; final gate must hold. |
| Ambiguous wrapper/PID exit is unsafe to retry automatically. | A lost launcher may have caused partially unknown side effects. | Wrapper exit taxonomy and explicit manual hold. | Kill/lost-receipt test creates a hold, never a PASS or automatic retry. |
| Strict execution must not rely only on agent/tool policy. | Recursive search/read and post-write tooling revealed escape paths. | External-lane wrapper owns process, workspace, environment, and approved runner invocation. | Boundary tests attempt forbidden file/tool behavior from the runner contract. |
| In-process validation can accidentally execute side effects. | Lint/LSP and dynamic file handling can run tools or dependencies. | Dry-run and config/evidence validators must be pure/read-only; wrappers run only after explicit lane admission. | Regression tests assert no process/network invocation in validation path. |
| Reviewers need different privileges from implementers. | An implementation restriction must not leak into an independent read-only review lane. | Separate lane profiles and wrapper contracts. | Development lane is write-capable; review lane has read-only contract and own profile. |
| A hold must survive normal recomputation/reconciliation. | Generic lifecycle recomputation can accidentally requeue unsafe work. | Sidecar hold with explicit release record; all dispatch decisions consult unreleased holds. | Reconciliation/restart test preserves hold until release command. |
| Admission must use the same criteria at preview and real launch. | Dry-run/preflight drift makes operational claims unreliable. | One normalized policy decision used by dry-run and lane launch. | Compare dry-run decision with actual launch acceptance for same inputs. |
| Candidate sizing/contract validation must use the real candidate at launch time. | A changed task/workspace can invalidate a prior preview. | Wrapper receives a freshly computed candidate manifest; receipt is rejected if current identity changes. | Modify input between dry-run and launch; launch blocks or recomputes safely. |
| Parent/capability admission must not reserve capacity for impossible work. | Bad reservation can starve runnable work. | Keep capacity policy outside core; validate profile availability before declaring a lane eligible. | Unavailable profile returns actionable blocked reason without resource reservation. |
| Test environments must isolate HOME/HERMES_HOME and preserve candidate identity. | Tests can otherwise mutate live state or test the wrong source. | Conductor integration harness uses private temporary homes and content-hash receipts. | Integration test asserts isolation and unchanged source identity. |
| Final review must receive a complete, frozen, parseable packet. | Terminated/incomplete review cannot count as approval. | Evidence exporter and review packet validator. | Incomplete packet/verdict fails closed. |
| Broad core changes create an upgrade and policy burden. | Oversized core façade growth became a blocking review issue. | No private core fork; documented extension boundary only. | Static scan and clean-upstream installation test. |

## Behaviors intentionally not copied verbatim

| Core-fork mechanism | Why not copy it | Replacement / decision |
|---|---|---|
| Atomic edits to internal Kanban claim/retry/reconcile transactions. | Unsupported private surface creates high upgrade risk. | Use external-lane readiness policy and wrapper pre-spawn validation; escalate only a proven irreducible atomic race as a narrow generic upstream proposal. |
| Private `kanban_db` / dispatcher monkeypatch compatibility. | A plugin must not depend on internal functions or test monkeypatch seams. | Public plugin/lane interfaces and contract tests against released Hermes. |
| Deny-listing individual Hermes file tools. | Tool receiver behavior and backend paths can evolve; per-tool restrictions are brittle. | Restrict the external runner's operating contract and use a small approved interface. |

## Archived evidence

- Core-fork recovery checkpoint: `/var/lib/hermes/.hermes/cache/scratch/autonomous-orchestrator-recovery/core-free-pivot-checkpoint-20261015T215802Z`
- The checkpoint contains base identity, tracked binary patch, untracked archive, changed-file hashes, and SHA-256 manifest.
- Historical test and review receipts remain evidence of discovered failure modes. They are not release approval for Conductor.

## Migration rule

A Conductor feature may be marked complete only after its corresponding row has a replacement test or an explicit documented non-equivalence. No safety lesson is considered retired solely because its original core implementation is abandoned.
