# Technical Debt Disposition

This assessment distinguishes valuable requirements from expensive implementation artifacts. The goal is to preserve the former and deliberately shed the latter before Hermes Conductor gains production behavior.

## Evidence snapshot

The archived private-fork candidate currently carries a large core delta, including roughly 1,756 added and 339 removed tracked lines across 21 tracked files, plus multiple untracked tests. The two principal internal facades remain oversized:

- `hermes_cli/kanban_db.py`: 4,702 lines
- `hermes_cli/kanban_db_dispatch.py`: 3,337 lines

That size and coupling are evidence that the candidate is a valuable requirements discovery artifact but a poor long-term extension boundary.

## Disposition matrix

| Item | Disposition | Reason | Conductor replacement / evidence |
|---|---|---|---|
| Broad `kanban_db.py` lifecycle/reconciliation changes | **Shed from active delivery path; retain archive** | Private transactional coupling and oversized façade maintenance create high update/rebase cost. | External-lane policy state, candidate receipts, and explicit holds; upstream proposal only for a proven atomic gap. |
| Broad `kanban_db_dispatch.py` spawn/reclaim/capacity changes | **Shed from active delivery path; retain archive** | Duplicates scheduler responsibilities already owned by Hermes and carries process-global/private-state risk. | Documented external worker lanes and a wrapper-owned runner contract. |
| Private monkeypatch compatibility | **Shed** | It tests/private-couples to symbols that are not an API contract. | Public integration contract tests against supported Hermes releases. |
| Per-tool deny lists for implementation restrictions | **Shed as the primary boundary** | New tools and backend paths can bypass a deny list; maintaining it is security debt. | Approved external wrapper interface, workspace/environment policy, and narrow runner inputs. |
| Exact-candidate evidence binding | **Keep** | It is a core correctness requirement independent of implementation. | Candidate manifest, canonical hash, signed-by-content receipt schema, mismatch tests. |
| Codex-before-Claude sequencing | **Keep** | It is a workflow quality requirement, not a core implementation detail. | Policy gate and lane launcher deny rules. |
| Manual hold on ambiguous runner exit | **Keep** | Prevents false success and unsafe automatic retries. | Hold/release state machine, exit taxonomy, recovery tests. |
| Separate implementation and reviewer contracts | **Keep** | Prevents privilege/restriction leakage across roles. | Distinct lane profiles and wrapper modes. |
| Private test gate runner that copies candidate files into a disposable Hermes tree | **Reduce and reimplement narrowly** | Strong isolation lesson, but its current form is tied to one candidate/worktree. | Reusable test fixture that creates private homes, clean upstream checkouts, and deterministic evidence fixtures. |
| Large accumulated regression suite tied to core behavior | **Mine, do not blindly port** | Some tests prove universal safety properties; others only prove private scheduler internals. | Map each test to a ledger behavior, then port only public-contract and safety scenarios. |
| Review packet builders/slice/retry scripts | **Consolidate** | Multiple one-off packet scripts risk format drift. | One versioned evidence package format and one exporter/verifier. |
| Documentation set | **Keep with a source-of-truth hierarchy** | Current docs are useful but could drift as implementation begins. | `spec-v0.1.md` is normative; delivery plan tracks sequence; risk and lessons registries track rationale. Every behavior change updates the spec first. |

## Debt prevented in the new repository

Before feature implementation expands, Conductor must avoid creating these common debts:

1. **One-off provider adapters.** Define a small normalized runner interface first; add providers through named profiles, not copy/paste lane logic.
2. **Duplicate policy decisions.** Dry-run, status, and actual lane admission must call the same pure policy evaluator.
3. **Unversioned state/config.** Persist schema versions and migration paths from the first sidecar record/config file.
4. **Opaque artifacts.** Use a stable JSON receipt schema and one evidence exporter/verifier.
5. **Optional-by-accident safeguards.** Put immutable rules in the policy engine, not only in README language or a preset.
6. **Documentation drift.** Treat the spec as normative and add a test/acceptance scenario for every material behavior.
7. **Premature framework building.** Do not add dashboards, generic workflow DSLs, multi-repo coordination, or a provider marketplace in v0.1.

## Decommission sequence

1. Preserve and verify the private-fork archive; never delete it before the migration ledger is complete.
2. Build the clean-upstream external-lane proof of concept.
3. Map every carried-forward requirement to a passing Conductor test or an explicit non-equivalence.
4. Mark the private candidate **archived, not deployable** once equivalent evidence exists for the supported-boundary design.
5. Keep the archive and lessons ledger for regression archaeology; stop maintaining or rebasing the core fork.

## Exit criterion

The core-fork path is fully shed only when Conductor's clean-upstream test matrix demonstrates the required safety/workflow behavior and the remaining non-equivalences have either been accepted by the owner or become narrow upstream API proposals.
