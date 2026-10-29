# Attempt 2 independent verification — October 29, 2026

**Verdict: READY_TO_SUBMIT for the supplied Project 2 requirements, with the explicit provenance/execution limits below.** No Attempt 2 grade is claimed. No agent redeployment, infrastructure recreation or repeat live AWS test was performed during finalization. One anonymous read-only HEAD request checked access to the recorded deployment artifact and returned HTTP 403.

## Source and evidence provenance

Corrected functional source commit: `d3ee0cdb510af5a10e695889dbb7386ce5a4f665`. Evidence branch commit: `c93aae6aedbcc580bbd60433e5577cf1263cd403`. Screenshot branch commit: `b6cad1ff3062a539e974ea49549dd14125c7f2be`. The latter descends from the former two and adds the five inspected screenshots. Source/tests are identical across these revisions and finalization makes no functional changes.

The screenshot branch removed four earlier response-only text files; finalization restores their original bytes as clearly labeled historical evidence. All 13 PNGs match their Git originals and all four text logs match `c93aae6`. [Evidence hashes](../evidence/EVIDENCE_SHA256.json) · [Visual-inspection metadata](../evidence/SCREENSHOT_INSPECTION_2026-10-29.json). Inspection metadata is a transcription/analysis, not raw AWS output or a replacement image.

`starter/main.py` SHA-256: `28887402ef78f0eddd84d40605390c52fc84479632e5bb169cc4c10a205d9deb`. This equals the local digest shown in the Runtime screenshot. The original Mac Desktop directory is not mounted here; only repository files and supplied evidence were inspected.

## Deployment and deployed-source boundary

[Runtime screenshot 14](../evidence/14_runtime_details.png) shows CustomerSupportAgent, status READY, version `2`, updated `2026-10-28T17:48:28.869077+00:00` (October 28, 23:18:28 IST). Its source location is:

- Bucket: `bedrock-agentcore-codebuild-sources-105833965496-us-east-1`
- Object prefix/key: `CustomerSupportAgent/deployment.zip`

Hosted order/Memory/loyalty captures consistently show `arn:aws:bedrock-agentcore:us-east-1:105833965496:runtime/CustomerSupportAgent-ZAsTqfF9MV`. [Order screenshot 09](../evidence/09_hosted_order.png) includes the real `uv run --no-sync agentcore invoke` command and successful ORD-001 response: SHIPPED, UPS, TRK987654321, October 31 delivery. It also shows READY in a Runtime listing. The source contains a module-level app, asynchronous decorated handler and `app.run()`.

**Deployed-package byte identity is not independently verified.** Runtime metadata plus a local digest are insufficient. Anonymous HTTPS HEAD access to the precise S3 artifact returned HTTP 403; no credentials were supplied and no artifact was downloaded. The author identifies this as the corrected deployment. This supports the target/status/version and hosted behavior, but no cryptographic package-to-source match is claimed. Under the supplied finalization instructions, disclosing this unavailable comparison is a limitation, not a reason to redeploy or block the demonstrated cloud-deployment criterion.

## Fresh Memory A/B: independently verified payloads and sessions

| Field | Session A | Session B |
| --- | --- | --- |
| Genuine screenshot | [10_memory_A.png](../evidence/10_memory_A.png) | [11_memory_B.png](../evidence/11_memory_B.png) |
| Customer ID | `CUST-MEM-20261029-61D1976B` | `CUST-MEM-20261029-61D1976B` |
| Application `session_id` | `attempt2-fresh-memory-A` | `attempt2-fresh-memory-B` |
| Runtime Session ID | `56CECE82-C455-409B-B50E-B19047A5D6B5` | `23A09AAB-BA5F-4FCA-A6FC-572D662FFB46` |
| Request ID | `744f7eae-1168-4b0f-bf69-a548628beaff` | `04e3a820-13af-4a6d-902b-9f1b33728c84` |
| Request content | Introduces Jane, short bullet-point preference, board games; asks to remember | Asks for name, style and category; does not repeat the saved facts |
| Response | Acknowledges all three facts | Recalls Jane, short bullet-point answers and board games |

The customer is fresh relative to the fixture actors; board games distinguishes this test from the older electronics preference. Both application IDs and actual Runtime IDs differ. Successful recall in B supports persistence/retrieval across these sessions; the unchanged hooks save the original user text and retrieve actor-level Memory. A raw Memory create-event response and extraction duration are not captured, so no internal service trace or measured delay is claimed.

The screenshots visibly contain payloads, Runtime IDs and responses, even though their literal shell invocation lines are cropped. Those images are authentic evidence of the displayed session workflow. No command history was invented. The October 28 response-only logs are preserved as historical material and are not substituted for this stronger fresh-actor test.

## Loyalty result: three distinct evidence levels

1. **Source contract:** `@tool` generates self-contained Decimal Python, redeems points in 500-point blocks under a 50% cap, applies tier discount after points, invokes `executeCode` with `clearContext=True`, parses the first valid result and requires all eight fields. Fallback is explicit, tier-only, with zero redemption/earnings and unchanged balance.
2. **Actual offline tool output:** [35-test final log](../evidence/16_offline_verification_2026-10-29.txt) includes JSON returned by the real calculator through a mocked service that executes the generated Python locally. The exact regression asserts every key/value.
3. **Hosted agent response:** [13_loyalty.png](../evidence/13_loyalty.png) shows an actual invocation command and the following displayed JSON, matching offline output. It does not expose a raw `executeCode` result event, sandbox session or service log. Raw remote execution is therefore not independently confirmed.

| Field | Verified source/offline output and hosted displayed JSON |
| --- | --- |
| `points_redeemed` | 4000 |
| `points_discount` | 40.0 |
| `tier_discount_pct` | 0.10 |
| `tier_discount` | 11.0 |
| `final_total` | 99.0 |
| `total_savings` | 51.0 |
| `points_earned` | 99 |
| `remaining_points` | 349 |

Arithmetic: $150 − $40 = $110; 10% of $110 = $11; final $99; 4250 − 4000 + 99 = 349. The old [October 28 transcript](../evidence/13_loyalty_attempt2.txt) says “10% ($15.00)” despite reporting $99 total. It remains unchanged and is explicitly superseded by the October 29 JSON capture. No raw tool result is inferred from an agent answer alone. The supplied instructions allow this execution-trace limitation to be stated; the required corrected schema/math are independently verified in source and executed regressions.

## Rubric basis, preservation and release

The prior Attempt 1 audit/PR summary records failures in deployment evidence, Gateway failure handling, Memory and loyalty schema, and passes in RAG, Browser and Reflection. The original reviewer attachment/full scoring document is not present. The [reviewer checklist](SUBMISSION_CHECKLIST.md) maps all seven identified criteria and all six scenarios from the archived official project instructions, without claiming coverage of unseen additional criteria.

The original license, attribution, upstream instructions, reflection, MemoryHook, RAG, Browser registration, Lambda sources, catalog, manifest and lockfile are preserved. All 35 offline regressions pass. Completed instructional TODO sections still retain their starter comments; no placeholder function implementation remains. Full production SDK imports are not tested by the stubbed suite; lockfile/dependency preservation and authentic hosted operation provide separate context.

All mandatory gates in the supplied finalization instructions pass within these declared evidence limits. The source-package comparison and raw remote Code Interpreter event remain unverified, nonblocking limitations; an additional AWS test is not requested. The final repository/ZIP checks and security scope are recorded in [validation](VALIDATION.md).
