# Attempt 2 resubmission checklist

[Reviewer matrix](RUBRIC_AUDIT.md) · [Original hosted invocation](../evidence/CLOUD_INVOCATION_ORIGINAL.md) · [Offline test log](../evidence/12_offline_regression_tests.txt) · [Evidence index](../evidence/README.md)

## Completed offline

- [x] Back up the original clean repository and Git history before editing.
- [x] Use a dedicated remediation branch based on latest main; do not overwrite main or rewrite history.
- [x] Handle Gateway context-entry/discovery failures, timeouts, connection errors, unexpected errors, empty tools and cleanup failures with safe user messages and diagnostic logging.
- [x] Preserve successful MCP tool discovery, registration, order tracking and simulated refunds.
- [x] Add fractional tier_discount_pct to the complete eight-field loyalty result.
- [x] Preserve correct post-points tier math, caps, redemption blocks and earning rates.
- [x] Parse the first SDK result's printed business JSON; keep explicit, consistent tier-only fallback.
- [x] Pass 35 offline tests, including all required numerical values.
- [x] Preserve RAG, Browser, MemoryHook, reflection, Lambda sources, manifest, lockfile and original license.
- [x] Link the original genuine cloud invocation near the beginning of the root README.
- [x] Preserve all eight original screenshots and distinguish their historical scope.
- [x] Follow the author's updated public-visibility/retained-configuration decision and record remaining exposure concerns.

## Required live gates — not yet completed

- [ ] Obtain explicit approval for AWS deployment and live testing.
- [ ] Confirm the educational account/profile and existing resources are accessible; report expiry or permission failures honestly.
- [ ] Deploy the updated agent and verify READY plus that the new code is hosted.
- [ ] Capture genuine hosted order invocation in `evidence/09_cloud_invoke_attempt2.txt`.
- [ ] Capture session A in `evidence/10_memory_session_A.txt`.
- [ ] Wait at least 30 seconds, then use a distinct session B with the same actor; capture genuine recall in `evidence/11_memory_session_B.txt`.
- [ ] Validate outputs, retain any failed attempts honestly, then rebuild the final ZIP and prepare the merge into main.

The three absent live transcript files are not placeholders and are not marked as successes. Original screenshot 08 supports a prior hosted invocation; it cannot prove the updated branch is deployed. Original local memory screenshot 04 is supplementary and does not replace hosted A/B evidence.

## Student submission

- [ ] Compare against any additional official rubric text not supplied here.
- [ ] Review the first-person 285-word reflection for accuracy.
- [ ] Review the ZIP's README, source, reflection, assets and clearly labeled evidence; do not submit a draft as fully verified.
- [ ] Submit manually through Udacity after the required evidence is complete or the genuine lab blocker is documented.

No Udacity submission or account access is performed by this task. No Attempt 2 Udacity pass is claimed.
