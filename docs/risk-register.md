# Risk Register and Technical Advisory Notes

This register captures risks that are easy to miss when building an upstream-compatible orchestration plugin. Each implementation milestone must review applicable open entries before declaring completion.

| ID | Risk | Why it matters | Control / decision |
|---|---|---|---|
| R1 | Plugin API assumption | A design can appear plugin-compatible while depending on an undocumented internal behavior. | Every integration starts with a clean-upstream proof using only documented APIs; static tests ban private Hermes imports and runtime rebinding. |
| R2 | False equivalence to atomic core enforcement | Observers and post-claim policy compensation cannot guarantee the same result as a pre-claim database veto. | Treat non-atomic gaps explicitly. Propose a narrow upstream primitive only after a reproducible unacceptable race is demonstrated. |
| R3 | Runner isolation theater | A hook can deny normal tool calls but cannot serve as the only OS/process boundary. | Put workspace/environment/process restrictions in the external lane wrapper; test escape attempts. |
| R4 | Evidence that is present but wrong | A review PASS is useless if it is bound to a different tree, config, or test run. | Use canonical candidate/config hashes; verify every dependent receipt before progression; make mismatch a hold. |
| R5 | Configuration becomes code execution | Arbitrary provider/model/command/path values enable accidental or malicious command injection. | Profiles are allow-listed named objects; use argument arrays; reject task-provided commands, paths, and credentials. |
| R6 | Provider and cost surprises | Users may select a model/provider that is unavailable, expensive, rate-limited, or unsuitable for final review. | Validate availability before spawn; show expected profile in dry run; expose timeout/budget/retry caps; keep a no-network local test mode. |
| R7 | Credential/data leakage | Prompts, logs, artifacts, and diagnostics can accidentally contain tokens or proprietary code. | Host-owned auth only; redaction tests; minimal receipt payloads; configurable retention; export preview before sharing. |
| R8 | Recovery creates false completion | Lost PID, malformed receipt, or restarted host can be mistaken for a successful runner. | Unknown state is always an explicit hold; receipts are idempotent, signed by content hash, and verified before PASS. |
| R9 | Upgrade drift | A plugin can remain source-compatible but semantically change as Hermes evolves. | Test declared floor and latest stable; add contract tests per extension surface; fail clearly on unsupported versions. |
| R10 | Sidecar/Hermes divergence | Plugin state can disagree with canonical task state after disablement, manual task action, or restoration. | Hermes is canonical; reconcile idempotently; expose diagnostic state; ensure disable/uninstall leaves task records usable. |
| R11 | Scope inflation | Building dashboards, every provider, notifications, and scheduler features before one trusted workflow delays real use. | Enforce v0.1 MVP boundary; require evidence from pilot users before adding a new subsystem. |
| R12 | Catalog rejection or loss of trust | Under-disclosed capabilities, binaries, mutable downloads, or broad permissions block listing and reduce adoption. | Maintain catalog checklist; source-only releases; exact commit pinning; complete security disclosure before every submission. |
| R13 | Branding/endorsement ambiguity | A name using Hermes may be read as official or endorsed. | Keep an explicit “unofficial, independent plugin” disclaimer; verify project naming/branding guidance before catalog submission. |
| R14 | Maintainer single point of failure | Public users need a way to report security issues, understand support expectations, and recover if maintenance pauses. | Add SECURITY, support, contribution, release, and deprecation policies before public beta. |
| R15 | Review ritual without real independence | “Codex then Claude” has little value if prompts are weak, packets are incomplete, or review outcomes are not actionable. | Freeze exact review packet; require structured verdicts; make defects blocking; use independent prompts and reviewer profiles. |

## Advisor guardrails

The following proposals should be challenged rather than accepted by default:

- A request to mimic all scheduler internals in a plugin: this is a hidden fork and should be rejected.
- A request to allow arbitrary shell commands in task/config data: use named approved runner profiles instead.
- A request to hide uncertainty by auto-retrying a lost worker: unknown runner outcome must remain a hold.
- A request to add telemetry for convenience: ship with no telemetry and justify any opt-in collection later.
- A request to submit to the catalog before the external-lane POC and disclosure audit: do not do it.
- A request to call a partial test shard a release approval: test scope must match the claim.

## Near-term advisory priorities

1. Build the smallest clean-upstream external-lane proof of concept before porting behavior from the prior core candidate.
2. Add a configuration schema and pure policy/evidence modules before spawning real providers.
3. Add security, contribution, and support policies before inviting external adoption.
4. Test one failure path as early as the happy path: missing receipt after a runner exits.
5. Validate product naming and catalog branding guidance before the first public-beta announcement.
