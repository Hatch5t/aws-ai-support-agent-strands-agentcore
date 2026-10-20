# Attempt 2 — reviewer-driven compliance audit

Updated 20 October 2026. The author's supplied Attempt 1 reviewer feedback supersedes the earlier pre-review audit. Udacity passed RAG, Browser, and reflection, and failed deployment evidence, Gateway failure handling, cross-session memory evidence, and Code Interpreter output fields. No Udacity account was accessed.

The earlier audit counted seven loyalty fields and did not check the reviewer's required `tier_discount_pct`. That was an omission; the current audit checks all eight fields. Successful local examples and an original hosted screenshot are not treated as proof that the remediated code is deployed or that the requested hosted memory workflow passed.

## Reviewer matrix

| Criterion | Attempt 1 | Attempt 2 status | Evidence |
| --- | --- | --- | --- |
| Cloud deployment | FAIL: hosted invocation evidence not accepted/located | Original genuine cloud evidence made prominent; updated deployment/invocation AWAITING APPROVAL | [Original hosted invocation](../evidence/CLOUD_INVOCATION_ORIGINAL.md), [screenshot 08](../evidence/08_cloud_invocation.png) |
| MCP Gateway | FAIL: insufficient failure handling | OFFLINE VERIFIED: connection/context entry, discovery, empty tools, cleanup, safe errors and logging | [gateway_tool_session](../starter/main.py#L583), [tests](../tests/test_remediation.py), [35-test log](../evidence/12_offline_regression_tests.txt) |
| Knowledge Base RAG | PASS | PRESERVED: source unchanged; 3 mocked regressions pass | [RAG function](../starter/main.py#L348), [screenshot 03](../evidence/03_rag.png) |
| Long-term Memory | FAIL: agentcore invoke evidence from two hosted sessions requested | Hook unchanged; existing local retry evidence preserved; hosted A/B evidence AWAITING APPROVAL | [MemoryHook](../starter/main.py#L166), [local screenshot 04](../evidence/04_cross_session_memory.png) |
| Code Interpreter | FAIL: required tier_discount_pct missing | OFFLINE VERIFIED: eight business fields, numerical regressions, result parsing and consistent fallback | [calculator](../starter/main.py#L399), [tests](../tests/test_remediation.py), [offline log](../evidence/12_offline_regression_tests.txt) |
| Browser | PASS | PRESERVED: initialization/registration unchanged and checked in successful Gateway path | [browser registration](../starter/main.py#L658), [screenshot 06](../evidence/06_agentcore_browser.png) |
| Reflection | PASS | PRESERVED: 285 body words, unchanged | [REFLECTION.md](../REFLECTION.md) |

“OFFLINE VERIFIED” means mock-based execution of the changed code. It is not an AWS result or a Udacity grade. Attempt 2 has not been reviewed by Udacity and is not yet a fully live-verified resubmission.

## Gateway remediation

`gateway_tool_session()` retains MCPClient and Streamable HTTP, then uses ExitStack to keep the connection open for agent execution. Its targeted handling includes construction, entering the context, and `list_tools_sync()`; connection cleanup is handled as well. TimeoutError, ConnectionError, and unexpected failures are logged with `logger.exception()`. Empty discovery is logged explicitly and rejected. Successful discovery logs the tool count with `logger.info()`; the named application logger enables INFO output.

Only Gateway setup/cleanup failures become GatewayUnavailableError. A downstream model/invocation error remains an agent error. Users receive a fixed availability message without URL, token, or exception detail. Eleven Gateway tests cover success, failures during both entry and discovery, empty results, constructor failure, cleanup failure, and correct classification of a model error. The existing order/refund tools remain registered on success.

## Structured loyalty output

The generated Python still uses Decimal, 500-point redemption blocks, a 50% order-value cap, tier discount after points, and the original earning rates. Its result now contains:

```text
points_redeemed, points_discount, tier_discount_pct, tier_discount,
final_total, total_savings, points_earned, remaining_points
```

The fraction is 0.00 for Silver, 0.10 for Gold, 0.15 for Platinum, and 0.00 for an unknown tier. The first Code Interpreter result event is still checked for errors. The handler reads printed business JSON from documented `structuredContent.stdout` or text content, checks the required keys, and exposes those fields at the tool-output top level rather than returning only the SDK wrapper. A nonzero exit code, malformed/incomplete output, missing event, or unavailable service takes the explicit fallback.

The fallback remains tier-only: no points redeemed or earned, unchanged points balance, tier rate/discount and final total, all eight keys, `fallback: true`, and a clear reduced-mode message. It does not claim successful sandbox execution.

The Gold / 4,250 points / $150 standard-order test asserts 4,000 redeemed, $40 points discount, $110 subtotal, 0.10 rate, $11 tier discount, $99 total, $51 savings, 99 earned points and 349 remaining. Additional tests cover all tiers, unknown tiers, zero/insufficient points, block rounding/cap, small orders, device/fresh/default earning rates, SDK result formats, and failure/fallback paths.

## Evidence requirements and remaining gates

1. Obtain explicit approval before any AWS deployment, infrastructure change, or live test.
2. Check authorized credentials/resources, deploy updated code through the correctly configured starter environment, and verify READY plus the hosted code version. Do not claim success from old deployment metadata.
3. Capture the real `uv run agentcore invoke` command and order response into `evidence/09_cloud_invoke_attempt2.txt`.
4. Invoke memory session A, wait at least 30 seconds for extraction, then invoke distinct session B for the same customer. Capture genuine outputs into `10_memory_session_A.txt` and `11_memory_session_B.txt`; investigate failures and retain them honestly.
5. If the lab has expired, report that blocker and retain the original successful cloud screenshot. Do not create empty or imaginary passing evidence.
6. After genuine live evidence is validated, rebuild the ZIP and prepare the merge into main. No force push, history rewrite, evidence deletion, or premature merge is required.

The supplied reviewer feedback is the current remediation basis. A separate complete official rubric is still unavailable. The original copyright/license remains unchanged. The author has confirmed public redistribution permission and requested public visibility while retaining source configuration; this confirmation does not alter the written license or constitute an independent legal verification.
