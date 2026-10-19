# Verified demonstrations

**8/8 screenshots present, readable, and reviewed.** These are the author's existing test captures, retained without image edits. The evidence is carried forward from `codex/initial-submission` to `main`.

The first six captures show local application invocations that still use AWS integrations. The last two show deployment and a hosted Runtime invocation. This review inspected the captures and source; it did not repeat live AWS operations.

## Evidence index

| Screenshot | Scenario | What the capture demonstrates | Execution | Verification |
| --- | --- | --- | --- | --- |
| [01_order_tracking.png](01_order_tracking.png) | Order tracking | `order-tracker___get_order`; `ORD-001`, `SHIPPED`, UPS, fixture tracking number, and estimated delivery | Local application | PASS |
| [02_refund_processing.png](02_refund_processing.png) | Simulated refund | `refund-processor___initiate_refund`; `ORD-002`, refund identifier, `APPROVED`, and $139.99 | Local application | PASS; simulated transaction |
| [03_rag.png](03_rag.png) | Knowledge Base RAG | `search_knowledge_base`; demonstration electronics policy: 15-day return window, original condition/accessories, and Prime return condition | Local application | PASS; displayed tool call and answer |
| [04_cross_session_memory.png](04_cross_session_memory.png) | Cross-session preference recall | Same `CUST-123` actor, distinct `memory-test-A` / `memory-test-B` sessions; successful retry recalls short bullet-point answers and electronics | Local application | PASS on successful retry; earlier failure retained |
| [05_loyalty_discount.png](05_loyalty_discount.png) | Loyalty arithmetic | `calculate_loyalty_discount`; 4,000 points redeemed, $40 points discount, $11 tier discount, $99 total, $51 savings, 99 earned points, and 349 remaining | Local application | PASS for tool call and numerical response; sandbox execution NOT VERIFIED |
| [06_agentcore_browser.png](06_agentcore_browser.png) | Live webpage retrieval | Six `browser` call labels; response identifies example.com, “Example Domain,” and its first paragraph | Local application | PASS for displayed tool calls and retrieved response; Safari window is separate |
| [07_deployment_success.png](07_deployment_success.png) | AgentCore deployment | `uv run agentcore deploy`, Direct Code Deploy output, “Deployment completed successfully,” and “Deployment Success” | Cloud deployment | PASS; trace-delivery warning also visible |
| [08_cloud_invocation.png](08_cloud_invocation.png) | Hosted order request | `uv run agentcore invoke`, hosted session/request details, and `ORD-001` response with `SHIPPED`, item, carrier, tracking, and delivery details | Cloud Runtime | PASS for hosted order invocation |

## Interpretation and limits

**Memory:** read the lower portion of screenshot 04 for the successful retry. The earlier recall says it cannot access the preferences; that attempt is not counted as a success. The later response recalls both preferences under a different session ID. No extraction-duration measurement or full Memory service trace is shown.

**Loyalty:** screenshot 05 shows the complete correct numerical response and calculator-tool selection. It does not display an `executeCode` result event, remote sandbox session, or trace proving the execution path. Source includes a reduced tier-only fallback. Do not infer independent sandbox verification from the agent's numerical answer.

**Browser:** the evidence is the terminal's `browser` calls and returned example.com content. The manually opened Safari window on the right is not represented as the managed AgentCore Browser session or its visual stream. The capture does not reveal the managed session ID or raw automation trace.

**Deployment:** screenshot 07 verifies the deployment-success report. It also includes a warning about X-Ray/CloudWatch trace-delivery configuration. Deployment success does not establish complete observability setup. A literal current `READY` status query is not shown; the author's READY statement is supported by the successful deployment and subsequent hosted invocation, not a fresh status check.

**Coverage:** screenshots 01–06 are local application demonstrations. Screenshot 08 establishes one cloud order-tracking invocation. The repository does not claim six independently repeated cloud tests, continuous current service availability, or production readiness.

## Security review

All eight images were inspected for sensitive material. Screenshots 07–08 contain account/resource identifiers, ARNs, operational paths, and request/session identifiers. These are not access keys, secret keys, session tokens, or bearer credentials; no such credential was visible in the captures. Identifiers alone do not grant access, so credential rotation or Git history rewriting is not warranted by these identifiers alone.

Keep the repository PRIVATE and limit reviewer access. Redact identifiers, local paths, and operational details before broader sharing. The unchanged source also contains a live Gateway endpoint with an unsigned educational client; this is a separate access risk requiring review before broader distribution. No active Gateway call was made to assess its live authorization.

No redaction was required for this private finalization, and no screenshots were altered or recreated. If a future redaction is needed, retain the original outside Git, label the redacted copy clearly, preserve genuine results, and review the staged image. Removing material in a later commit does not remove it from earlier commits; rewriting history requires explicit approval.
