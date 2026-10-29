# Evidence index — Attempt 2 final submission

Verified October 29, 2026. **13 genuine, unmodified screenshots are included:** eight original captures and five current hosted captures from `attempt2-screenshots-20261029` (`b6cad1f`). Four original October 28 response-only transcripts are also retained for audit. No screenshot or AWS response was fabricated, regenerated, edited or redacted.

[Reviewer criterion mapping](../docs/SUBMISSION_CHECKLIST.md) · [Detailed independent inspection](../docs/ATTEMPT2_VERIFICATION_REPORT.md) · [Evidence hashes](EVIDENCE_SHA256.json) · [Screenshot inspection metadata](SCREENSHOT_INSPECTION_2026-10-29.json)

## Current reviewer-facing hosted evidence

| Original file | Verified image contents | Scope and limits |
| --- | --- | --- |
| [09_hosted_order.png](09_hosted_order.png) | Real `uv run --no-sync agentcore invoke` command for ORD-001; CUST-123, application session `attempt2-order-final`; hosted response SHIPPED, UPS, TRK987654321, delivery October 31, 2026; READY Runtime listing | PASS: command, target Runtime and hosted order response visible |
| [10_memory_A.png](10_memory_A.png) | Payload introduces Jane, short bullet-point answers and board games for fresh actor `CUST-MEM-20261029-61D1976B`; app session `attempt2-fresh-memory-A`; Runtime A `56CECE82-C455-409B-B50E-B19047A5D6B5`; acknowledgement | PASS: payload/actor/application and Runtime IDs and acknowledgement visible. Literal shell invocation line cropped; no raw Memory write event shown |
| [11_memory_B.png](11_memory_B.png) | Same actor; app session `attempt2-fresh-memory-B`; Runtime B `23A09AAB-BA5F-4FCA-A6FC-572D662FFB46`; request does not repeat facts; response recalls Jane, short bullet points and board games | PASS: fresh test with both session layers distinct and accurate recall. No measured extraction delay or internal Memory trace claimed |
| [13_loyalty.png](13_loyalty.png) | Actual invoke command and hosted JSON with all eight required keys: 4000 redeemed, $40 points, 0.10 tier fraction, $11 tier discount, $99 total, $51 savings, 99 earned, 349 remaining | PASS for displayed hosted JSON/schema/math; raw Code Interpreter execution event not shown. Source and executed offline output independently verify the tool contract |
| [14_runtime_details.png](14_runtime_details.png) | CustomerSupportAgent READY, version 2; updated October 28; source S3 bucket/object; local main.py SHA-256 | PASS for displayed deployment metadata. Does not prove byte identity of the deployed archive; anonymous artifact access returned 403 |

All hosted captures identify the existing CustomerSupportAgent Runtime in account 105833965496, us-east-1. The Runtime update is `2026-10-28T17:48:28.869077+00:00`. Screenshot 14 is the current READY/version metadata evidence; it is not relabeled as a fresh terminal “Deployment Success” log. The original successful deployment log remains screenshot 07.

The JSON in screenshot 13 is the agent's displayed response, not a raw sandbox event. [Actual offline calculator output](16_offline_verification_2026-10-29.txt) is separately labeled and contains the same eight values. The [inspection report](../docs/ATTEMPT2_VERIFICATION_REPORT.md) keeps these evidence levels distinct.

## Preserved historical evidence

| Original file | Genuine observation | Qualification |
| --- | --- | --- |
| [01_order_tracking.png](01_order_tracking.png) | Local order MCP call and ORD-001 SHIPPED, UPS/tracking/delivery | Original local application test, not the current hosted run |
| [02_refund_processing.png](02_refund_processing.png) | Refund MCP call, ORD-002, APPROVED, $139.99 and refund ID | Preserved accepted simulated-refund evidence; no real payment |
| [03_rag.png](03_rag.png) | Knowledge Base tool call and electronics 15-day return policy | Preserved reviewer-accepted RAG evidence |
| [04_cross_session_memory.png](04_cross_session_memory.png) | Local A/B electronics/style preference retry succeeds after earlier failed recall | Earlier failure remains visible; superseded by the new fresh-actor hosted A/B test |
| [05_loyalty_discount.png](05_loyalty_discount.png) | Local calculator selection and correct numerical answer | No raw sandbox event; predates added `tier_discount_pct`; superseded by current JSON screenshot 13 |
| [06_agentcore_browser.png](06_agentcore_browser.png) | Browser tool calls and retrieved example.com heading/paragraph | Preserved reviewer-accepted Browser evidence; separate Safari window is not claimed as managed Browser stream |
| [07_deployment_success.png](07_deployment_success.png) | Original Direct Code Deploy success report | Historical; trace-delivery warning retained; not an October 29 capture |
| [08_cloud_invocation.png](08_cloud_invocation.png) | Original hosted ORD-001 command and shipping response | Historical, prior to Attempt 2 corrections |
| [CLOUD_INVOCATION_ORIGINAL.md](CLOUD_INVOCATION_ORIGINAL.md) | Readable transcription of screenshot 08 | Authored transcription, not a raw new terminal log |

The original accepted [REFLECTION.md](../REFLECTION.md) remains unchanged at 285 body words.

## Historical October 28 transcripts and offline records

| File | Classification |
| --- | --- |
| [09_cloud_invoke_attempt2.txt](09_cloud_invoke_attempt2.txt) | Genuine older hosted shipping response, no input command/payload; superseded by current order screenshot |
| [10_memory_session_A.txt](10_memory_session_A.txt) | Genuine older Jane/preference acknowledgement; incomplete command/actor/application-ID context |
| [11_memory_session_B_distinct_runtime.txt](11_memory_session_B_distinct_runtime.txt) | Genuine older distinct-Runtime recall; new October 29 screenshots provide stronger fresh-actor/payload evidence |
| [13_loyalty_attempt2.txt](13_loyalty_attempt2.txt) | Genuine historical inconsistent answer: says 10% ($15.00) despite $99 total. Retained unchanged; not presented as the passing current result |
| [ATTEMPT2_TRANSCRIPT_INSPECTION.json](ATTEMPT2_TRANSCRIPT_INSPECTION.json) | Earlier text-log hashes and extracted identifiers/missing-field findings; inspection metadata, not AWS output |
| [12_offline_regression_tests.txt](12_offline_regression_tests.txt) | Preserved original actual 35-test run |
| [16_offline_verification_2026-10-29.txt](16_offline_verification_2026-10-29.txt) | Final actual 35/35 offline test output plus direct calculator JSON from locally executed generated Python; no AWS invocation |
| [VALIDATION_SUMMARY.json](VALIDATION_SUMMARY.json) | Final package, links, staged-content and credential-scan checks; generated validation metadata |

All four historical text logs match their bytes in `c93aae6`. Restoring them alongside current screenshots preserves the audit trail without duplicating current scenario claims.

## Security and authenticity

All 13 PNGs were visually inspected and OCR-scanned. Current/staged text, all reachable preexisting Git history and ZIP contents were scanned for credential patterns. No AWS access keys, secret/session-token candidates, private keys or other credential candidates were detected. OCR/custom pattern scanning is not a guarantee against every secret format. Hashes verify preservation, not independent authentication of AWS service internals.

Operational metadata remains visible: author/machine paths, account IDs, ARNs, Runtime/request IDs and artifact locations. These are not authentication credentials. The public unsigned Gateway endpoint in the preserved source is a separate access risk requiring owner review; no live access probe, visibility change or infrastructure security change was performed.
