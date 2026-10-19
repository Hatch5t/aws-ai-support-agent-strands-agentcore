# Test and deployment evidence

**Screenshot evidence status: PENDING.** The author will add the actual captures manually. This directory intentionally contains no generated or placeholder screenshots and no broken image embeds.

The author reports six successful local scenarios, Runtime READY status, and a successful cloud order invocation. Those statements are not substitutes for reviewer-visible captures. Full all-six cloud testing and independent Code Interpreter execution are not claimed.

## Required filenames

| Filename to add | Must demonstrate | Current status |
| --- | --- | --- |
| `01_order_tracking.png` | Local `ORD-001` request and response, shipping status, UPS carrier, and fixture tracking number; dates may vary | PENDING |
| `02_refund_processing.png` | Local simulated refund request for `ORD-002`, refund identifier, approval, and amount; clearly label it simulated | PENDING |
| `03_rag.png` | Local product/policy query, relevant Knowledge Base retrieval/tool evidence, and grounded response | PENDING |
| `04_cross_session_memory.png` | First session saves a synthetic name/preference; second session uses the same actor with a different session and recalls it; show retry/extraction timing if applicable | PENDING |
| `05_loyalty_discount.png` | Gold, 4,250 points, $150 standard order; all seven expected values; distinguish complete output from tier-only fallback | PENDING |
| `06_agentcore_browser.png` | Browser tool visiting an actual webpage and reporting the retrieved title/content; include URL and execution context without exposing private service endpoints | PENDING |
| `07_deployment_success.png` | AgentCore Runtime deployment completes and the intended Runtime reaches READY; redact account-specific identifiers | PENDING |
| `08_cloud_invocation.png` | Deployed Runtime is invoked for `ORD-001` and returns the corresponding order-tracking response; clearly identify cloud execution | PENDING |

Expected loyalty values: 4,000 points redeemed, $40 points discount, $11 tier discount, $99 final total, $51 savings, 99 points earned, and 349 remaining points. A numerical response alone does not independently establish Code Interpreter execution. Include execution-level tool/session evidence in the capture or a separately reviewed supporting artifact if you want to make that stronger claim.

## Adding evidence safely

1. Use your actual existing test captures. If additional execution is needed, perform it only with appropriate AWS authorization; no agent calls or deployments were run to create this repository.
2. Redact credentials, session tokens, account IDs, ARNs, Gateway endpoints, sensitive URLs, and real customer details. Avoid capturing browser address bars or terminal history containing secrets.
3. Save each reviewed image directly in this directory under the recommended filename. The ignore rules permit PNG/JPG evidence files.
4. Review the image content and update its table row from PENDING only when it actually demonstrates the required behavior. Update the root README's evidence status consistently.
5. Commit and push evidence to this same private repository. Check staged files before publication; `.gitignore` is not a secret scanner.

Do not add fake images, copied screenshots from other projects, raw deployment configuration, dependency ZIPs, or credential-bearing logs. Keep original full-resolution captures privately if the submitted image is redacted or cropped.
