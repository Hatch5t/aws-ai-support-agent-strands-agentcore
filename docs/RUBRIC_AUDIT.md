# Attempt 2 reviewer-driven rubric audit

Verified October 29, 2026. **READY_TO_SUBMIT for the supplied requirements, with evidence limits stated below.** This is an independent source/evidence audit, not an Attempt 2 Udacity grade. Original Attempt 1 outcomes are preserved from the prior audit/PR summary; the original reviewer attachment and complete standalone scoring document are unavailable. The [archived project instructions](upstream/UDACITY_PROJECT_INSTRUCTIONS.md) and the author's current requirements supply the detailed acceptance checks.

## Reviewer matrix

| Criterion | Recorded Attempt 1 result | Verified Attempt 2 result | Source, tests and genuine evidence |
| --- | --- | --- | --- |
| A. Deploy an AI agent to cloud Runtime | FAIL: hosted evidence missing/unclear | PASS: module app, async decorated entrypoint and app.run; existing Runtime READY version 2, October 28 update; current hosted order command/response | [main.py](../starter/main.py#L53), [entrypoint](../starter/main.py#L631), [server](../starter/main.py#L714), [order 09](../evidence/09_hosted_order.png), [Runtime 14](../evidence/14_runtime_details.png) |
| B. MCP Gateway | FAIL: insufficient error handling | PASS: MCPClient/Streamable HTTP, API-backed orders and Lambda-backed refunds, successful discovery logging; failure/empty-list/cleanup handling, safe fixed message; 11 offline cases pass | [gateway_tool_session](../starter/main.py#L583), [Gateway tests](../tests/test_remediation.py#L76), [hosted order](../evidence/09_hosted_order.png), [accepted refund](../evidence/02_refund_processing.png) |
| C. Knowledge Base RAG | PASS | PRESERVED PASS: Retrieve/passage joining, missing-ID guard and no-results behavior; 3 offline regressions | [RAG](../starter/main.py#L348), [tests](../tests/test_remediation.py#L310), [original RAG 03](../evidence/03_rag.png) |
| D. Long-term Memory | FAIL: hosted A/B evidence requested | PASS: fresh actor, same customer, different application IDs and actual Runtime IDs; B recalls Jane/style/board games without facts repeated in request | [MemoryHook](../starter/main.py#L166), [A 10](../evidence/10_memory_A.png), [B 11](../evidence/11_memory_B.png), [exact identifier comparison](ATTEMPT2_VERIFICATION_REPORT.md#fresh-memory-ab-independently-verified-payloads-and-sessions) |
| E. Code Interpreter loyalty tool | FAIL: missing tier_discount_pct | PASS for required implementation/schema/math: @tool, self-contained Python, executeCode/clearContext, complete eight-field JSON and explicit fallback; 21 loyalty regressions; hosted displayed JSON matches | [calculator](../starter/main.py#L399), [schema/parser](../starter/main.py#L516), [exact regression](../tests/test_remediation.py#L205), [actual offline tool output](../evidence/16_offline_verification_2026-10-29.txt), [hosted JSON 13](../evidence/13_loyalty.png) |
| F. AgentCore Browser | PASS | PRESERVED PASS: initialization/registration unchanged, covered by successful-tool regression; accepted browser calls/content preserved | [registration](../starter/main.py#L658), [successful-tools test](../tests/test_remediation.py#L113), [original Browser 06](../evidence/06_agentcore_browser.png) |
| G. Written reflection | PASS | PRESERVED PASS: original 285-word body covers design decision, dependency/deployment challenge and production controls | [REFLECTION.md](../REFLECTION.md) |

All 35 existing regressions pass: 11 Gateway + 21 loyalty + 3 RAG. They stub external services; hosted evidence is independently supplied by the genuine images. No accepted Refund/RAG/Browser/Reflection test was unnecessarily repeated against AWS.

## Gateway review

The scoped helper constructs/enters MCPClient, calls list_tools_sync and keeps transport open through agent execution. TimeoutError, ConnectionError and unexpected setup/discovery exceptions are logged with logger.exception and become GatewayUnavailableError. Empty/None discovery is rejected with a warning; malformed/unexpected discovery exceptions are caught. Cleanup is protected. Successful discovery logs its tool count at INFO. A bad tool object that fails later registration reaches the generic logged agent-error path; no claim of complete MCP schema validation is made.

Users receive “The order and refund services are temporarily unavailable. Please try again later.” for classified Gateway failures, without endpoint/token/exception details. Downstream model failures remain logged agent errors and get a separate safe message. Tests cover construction, context entry, discovery, timeouts/connections, unexpected failures, empty tools, cleanup, successful order/refund registration and model-error separation. API-backed order and direct Lambda refund invocation evidence are both retained. No live Gateway fault was induced.

## Eight-field loyalty contract

Required keys: points_redeemed, points_discount, tier_discount_pct, tier_discount, final_total, total_savings, points_earned and remaining_points. The tier rate is fractional: Gold 0.10, not 10. The exact regression and actual offline JSON assert 4000 redeemed/$40, $110 subtotal, $11 tier discount, $99 final total, $51 savings, 99 earned and 349 remaining. Tier discount follows points redemption in source.

The tool checks the result event/error/exit status, extracts JSON from stdout/text and validates required keys. Invalid or unavailable execution returns explicit tier-only fallback with all eight fields, zero redeemed/earned and unchanged balance. It does not invent successful sandbox execution.

[Current screenshot 13](../evidence/13_loyalty.png) shows a complete matching agent JSON response. The older [October 28 transcript](../evidence/13_loyalty_attempt2.txt) with the incorrect $15 tier phrase is retained unchanged as historical evidence. A displayed agent response is not a raw Code Interpreter event; remote sandbox execution remains unconfirmed at that trace level. Source and locally executed regressions independently prove the corrected structured result. This limitation is disclosed under the author's finalization instructions and does not erase the verified implementation/schema checks.

## Deployment provenance and release limits

Runtime details show READY/version 2 and October 28 update plus S3 artifact location. The local main.py digest equals the digest displayed in screenshot 14. These facts do not prove deployed-source byte identity. Anonymous read-only artifact access returned HTTP 403; no archive could be compared, and no source-match claim is made. The [verification report](ATTEMPT2_VERIFICATION_REPORT.md) records the precise boundary and actual Memory IDs. Literal Memory shell commands are cropped, but original payloads, both ID layers and responses are visible; no history was reconstructed.

The above mappings cover all seven criteria identified in supplied review history and all six official project scenarios. They cannot certify unseen additional rubric requirements. Original source architecture, dependencies, attribution/license and accepted evidence are preserved. [Submission checklist](SUBMISSION_CHECKLIST.md) · [Validation/security](VALIDATION.md) · [Evidence index](../evidence/README.md).
