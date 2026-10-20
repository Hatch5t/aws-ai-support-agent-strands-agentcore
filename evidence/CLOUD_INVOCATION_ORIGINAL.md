# Original successful hosted invocation — prior to Attempt 2

**This is genuine original cloud evidence, not a claim that the updated Attempt 2 code is deployed.** The reviewer reported missing/unclear hosted invocation evidence in Attempt 1. The existing capture is linked prominently here and from the root README.

[Open the original full-resolution cloud invocation screenshot](08_cloud_invocation.png)

The command and response below are transcribed from that screenshot for readability; this Markdown file is not a newly captured raw terminal log.

```bash
uv run agentcore invoke '{"prompt":"Hello! Can you help me track order ORD-001?","customer_id":"CUST-123","session_id":"cloud-test-1"}'
```

The screenshot shows the hosted agent panel, session/request metadata, and this response:

```text
Order ID: ORD-001
Status: SHIPPED
Item: Wireless Headphones Pro ($89.99)
Carrier: UPS
Tracking #: TRK987654321
Estimated Delivery: October 20, 2026
```

The response is followed by the terminal prompt, with no invocation error visible. This supports the original hosted execution, not the current service state or deployment of the remediation branch. The unchanged [deployment screenshot](07_deployment_success.png) is separate evidence and retains its trace-delivery warning.

## Attempt 2 live evidence status

Fresh deployment and live tests require the author's explicit approval. The files below will be created only from genuine executions:

- `09_cloud_invoke_attempt2.txt`: exact hosted invocation command and real response after deployment of updated code.
- `10_memory_session_A.txt`: genuine first-session `agentcore invoke` output.
- `11_memory_session_B.txt`: genuine later-session recall output using the same actor and a different session ID.

These three files are not present yet and are not represented as successful tests. Existing local memory screenshot 04 remains supplementary; it is not substituted for the reviewer-requested hosted two-session invocation evidence.
