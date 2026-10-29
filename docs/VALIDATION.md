# Attempt 2 final validation — October 29, 2026

**READY_TO_SUBMIT within the supplied requirements and the explicit limits below.** Corrected application source `d3ee0cd` is unchanged. Evidence ancestry `c93aae6` → `b6cad1f` is integrated; current screenshots supersede weaker historical results while preserving their original bytes. The original Mac Desktop path is not mounted in this environment.

## Functional verification

| Gate | Result |
| --- | --- |
| Regression suite | `python3 -m unittest discover -s tests -v`: 35/35 PASS; 11 Gateway, 21 loyalty, 3 preserved RAG cases |
| Actual run output | [Final log and direct offline calculator JSON](../evidence/16_offline_verification_2026-10-29.txt); external service dependencies stubbed, generated Python really executed locally |
| Python/import compatibility | All Python sources parse; actual app module imports under SDK stubs in each regression. Audit Python 3.12.14; project requires >=3.13 and dependencies/lockfile are preserved. No full production SDK import or new 3.13 installation is claimed |
| Source completeness | Module-level BedrockAgentCoreApp, async decorated entrypoint, app.run, configured identifiers, hooks and tools present. Original TODO labels/comments remain, but required implementation sections are complete |
| Gateway | MCP connection/discovery/registration, INFO success count, logged exceptions, timeout/connection/unexpected/empty/cleanup errors and safe messages covered. No live outage was induced |
| Loyalty | All eight keys and exact Gold values verified in direct offline output, source and regressions; hosted screenshot shows matching agent JSON. Tier discount applied after points |
| Memory | New screenshots verify same fresh actor, distinct app and Runtime IDs, introduction/acknowledgement and accurate later recall without saved facts in B request |
| Preserved accepted material | Namespace helper, MemoryHook and RAG AST-identical to original main; Browser construction/registration unchanged; accepted Refund/RAG/Browser/Reflection evidence retained |
| File identity | Lambda sources/schema, manifest, lockfile, catalog, permission helper, original license, archived instructions and reflection match their pre-finalization originals; reflection body 285 words |
| Genuine screenshots/logs | 13 original PNGs visually inspected and hash-matched to their Git originals; four older logs byte-identical to c93aae6 and labeled historical |
| Documents/data | Python, dependency TOML and schema JSON parse; relative file/heading/source anchors and README image references checked; linked repositories resolved through GitHub |

## Hosted proof and what it does not prove

[Runtime screenshot 14](../evidence/14_runtime_details.png) shows READY/version 2 and update `2026-10-28T17:48:28.869077+00:00`, with source S3 bucket/object. Hosted captures identify the same existing Runtime ARN in account 105833965496. Source SHA-256 equals the **local** digest shown in the image. Anonymous HTTPS HEAD access to the recorded deployment ZIP returned HTTP 403; no deployed archive was obtained. Source/package byte identity remains **unverified**, as explicitly permitted to disclose under the finalization instructions.

The fresh [loyalty JSON screenshot](../evidence/13_loyalty.png) supersedes the incorrect $15 phrase in the unchanged [historical transcript](../evidence/13_loyalty_attempt2.txt). It is a hosted agent response, not a raw executeCode result. Source and executed offline tool output independently verify all eight fields and arithmetic; raw remote execution is not asserted. Memory screenshots show payloads and both session layers but omit literal shell invoke lines and raw Memory write/extraction events. These are documented evidence limits, not hidden passes or fabricated logs.

No agent redeployment, infrastructure creation, IAM write, refund action, memory write or repeat AWS functional test was performed by finalization. The single read-only artifact-access attempt is described above. No repository visibility change or Udacity submission was performed.

## Security scope

The custom scanner checked all six preexisting reachable Git commits (50 unique non-image blob/commit objects), all working/staged final text, and 13 unique historical PNG blobs through Tesseract OCR. All 13 screenshots were also visually reviewed; originals were never modified. The final tree/commit metadata and ZIP are checked before delivery. The generated [validation summary](../evidence/VALIDATION_SUMMARY.json) records the exact scan base/tree and package checks. No credential candidates were detected.

Patterns include AWS key IDs and secret/session-token assignments, private keys, GitHub tokens, JWTs, long bearer strings, signed-URL credential parameters and generic long secret assignments. No candidate values were printed or published. This was a custom pattern scan, not Gitleaks; OCR and regex cannot guarantee detection of every secret format. Unmounted Mac files and unreachable/deleted remote objects were not scanned. Account/resource IDs, ARNs, usernames/paths, Runtime/request IDs and artifact locations remain as operational metadata; these are not credentials.

**Owner intervention:** public source contains the unsigned educational Gateway endpoint, assumes NONE authorization, accepts caller-controlled customer IDs and bypasses interactive consent. Public copies may allow unintended fixture-tool access while the endpoint is active. No live Gateway probe was made. Review authorization or disable the educational endpoint when no longer needed; changing Git visibility or deleting a URL does not revoke access or erase history. Logs may retain prompts/tool payloads, so fixture-only use and access/retention controls remain appropriate. No security configuration or history rewrite was made, and no credential rotation is requested solely because identifiers are visible.

## Repository and package checks

Final work retains the evidence-branch ancestry and uses non-forced fast-forward updates to the remediation branch and main after the gates pass. Remote branch commits/tree and representative content are read back and compared with the scanned local tree. The final delivery report records exact commit/branch and remote status; no new branch or duplicate screenshot set is required.

The ZIP uses an explicit tracked-file allowlist plus a generated SHA-256 member manifest. It includes code, manifest/lockfile, tests, reflection, notices, maintained docs and all genuine evidence. It excludes Git metadata, environments, credentials, private AWS/AgentCore configuration, generated deployment/dependency archives, caches, intermediate OCR and machine-specific state. CRC/readback, path traversal/duplicate-member checks, byte identity and all included local references are verified. The final size and ZIP SHA-256 are reported with delivery.

All seven supplied rubric criteria and all six official scenarios are mapped in the [reviewer checklist](SUBMISSION_CHECKLIST.md). Original reviewer attachment/full standalone rubric is unavailable, so unseen additional criteria are not certified. No Attempt 2 Udacity result is claimed.
