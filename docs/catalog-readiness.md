# Hermes Plugin Catalog Readiness

This checklist tracks the admission policy in `NousResearch/hermes-agent/plugin-catalog/README.md`. The catalog listing is intentionally deferred until Conductor's external-worker-lane proof of concept is complete.

## Already satisfied

- [x] Public HTTPS repository.
- [x] Native `plugin.yaml` plus Python `__init__.py` entrypoint.
- [x] Public API boundary only; no private Hermes imports or core overrides.
- [x] Exact Apache-2.0 license text.
- [x] Truthful `requires_hermes: ">=0.21.6"` floor, tested locally.
- [x] Versioned manifest, README, architecture, and configuration example.
- [x] No dependencies, binary payloads, bundled bytecode, self-updater, telemetry, credential reads, network calls, shell execution, or background processes in `0.1.0`.
- [x] `hermes plugins validate --install-deps` passes locally.

## Required before catalog PR

- [ ] Implement and test the first documented external worker lane against a clean released Hermes checkout.
- [ ] Declare every registered tool, hook, middleware item, and required environment variable in the catalog entry `capabilities` block.
- [ ] Re-run `hermes plugins validate --install-deps` at the exact commit to pin; resolve every warning, not only failures.
- [ ] Add automated validation on supported Python and Hermes versions.
- [ ] Update README risk disclosures for all released behavior: network endpoints, shell commands, background work, data paths, credential routes, and telemetry.
- [ ] Confirm all credentials use Hermes secret/provider routes; never inspect environment files, auth stores, vendor CLI state, browser profiles, or keychains.
- [ ] Confirm unattended runs fail/timeout cleanly and never bypass Hermes approvals.
- [ ] Create a source-only release commit; no compiled binaries, committed bytecode, or opaque archives.
- [ ] Prepare a catalog YAML entry with the full 40-character release commit SHA, matching version, maintainer, category `automation`, and exact capabilities.
- [ ] Submit the catalog entry as a maintainer-reviewed PR to `NousResearch/hermes-agent`; do not rely on branches, tags, automated ingestion, or self-update behavior.

## Release procedure

1. Update version, README disclosures, compatibility range, and changelog in one source-only commit.
2. Run validation and integration tests against the exact commit.
3. Create the catalog entry pinned to that full commit SHA.
4. Open a catalog PR describing all Hermes extension surfaces and user-visible risk disclosures.
5. Treat every catalog update as a new reviewed SHA-bump PR.
