# Engineering notes

The detailed [starter README](../starter/README.md) is the implementation and operations reference. These notes identify the most consequential behaviors without repeating its complete runbooks.

## Source map

| Component | Source | Significant behavior |
| --- | --- | --- |
| Runtime entry point | [main.py](../starter/main.py) | One app; fresh agent and Gateway discovery per request |
| Memory integration | [MemoryHook](../starter/main.py) | Message-added retrieval and after-invocation saving |
| RAG / loyalty tools | [main.py](../starter/main.py) | Explicit KB Retrieve and sandbox execution/fallback |
| Orders | [order_tracker.py](../starter/lambda/order_tracker.py) | REST proxy event routing; fixture records |
| Refunds | [refund_processor.py](../starter/lambda/refund_processor.py) | Direct Gateway tool dispatch; simulated results |
| Refund definitions | [lambda_schema](../starter/lambda/lambda_schema) | Three tools with required/optional argument definitions |
| IAM helper | [setup_permissions.py](../starter/setup_permissions.py) | Source/config parsing, preview, scoped inline policy application |

## Lifecycle and failure handling

Module import initializes the model and AWS clients; syntax checks should not import the application. A non-empty prompt is required. Missing customer/session IDs become UUIDs, which means anonymous invocations do not automatically share the same customer memory.

The handler discovers Gateway tools before reasoning. Gateway setup/discovery/cleanup errors are now classified separately and return a safe order/refund availability response; empty discovery is not considered success. The MCP transport and successful tool list are preserved. It returns only the first assistant content block's text, and a caught exception returns a generic text error. Test response content and tool traces rather than relying on HTTP status alone.

The current environment sets `BYPASS_TOOL_CONSENT=true`. This permits headless operation, but it provides no authorization or business approval mechanism.

## Memory correctness

`get_namespaces()` reads `namespaceTemplates`, with `namespaces` as a compatibility fallback. Retrieval formats actor/session placeholders and requests up to five records per strategy namespace. The hook skips tool results and preserves `_original_user_query` before injecting context, then saves the original query rather than the augmented message.

The configured project strategies are semantic facts and user preferences. Extraction is asynchronous; screenshot 04 shows an earlier failed recall and a later successful retry between `memory-test-A` and `memory-test-B`. The complete raw session history is not read back by this implementation. Keep a stable actor ID, separate payload session IDs for cross-session tests, and distinguish these from a Runtime transport session ID.

## Loyalty contract

| Rule | Implementation |
| --- | --- |
| Redemption unit | 500 points; $0.01 per point |
| Redemption cap | 50% of order value, rounded down to a 500-point block |
| Tier discount | Silver 0%, Gold 10%, Platinum 15%; applied after points |
| Earning multiplier | Standard 1×, device 2×, fresh 5× on the final price |
| Monetary rounding | Decimal, two places, `ROUND_HALF_UP` |
| Complete output | Redeemed points, points discount, tier_discount_pct fraction, tier discount, total, savings, earned/remaining points |
| Error path | Local tier discount only; eight keys, zero points redeemed/earned, unchanged balance, `fallback: true` |

For the reported Gold / 4,250 points / $150 standard order: redeem 4,000 points, subtract $40, apply $11 tier discount, pay $99, save $51, earn 99 points, and finish with 349 points. This expected result is a calculation contract, not independent evidence that `executeCode` ran remotely.

## Python 3.13 and Linux ARM64

The manifest pins `lazy-object-proxy==1.12.0`; the lockfile includes a CPython 3.13 ARM64 Linux wheel. The original local dependency ZIP was previously inspected and contained its matching Linux ARM64 extension. That ZIP is excluded from this repository.

The author identifies native dependency compatibility as the deployment failure that required resolution. The exact earlier failing version/error transcript is unavailable, so it is not reconstructed here. A local macOS install is insufficient proof of target compatibility.

The Python Starter Toolkit is locked to `0.3.14`, and its installed help warns that it is deprecated. Reproduction uses that project's Python CLI, not the newer npm CLI project format. The inspected packager compiles manifest requirements and installs binary-only packages for Linux ARM64. It hashes `uv.lock` for cache invalidation but does not establish frozen transitive resolution during deployment. Local `uv sync --locked` and deployment packaging must therefore be evaluated separately.

## Permissions and state changes

The helper's `--dry-run` reads local files and prints a policy without AWS calls. Its normal mode validates account/role/resource consistency and writes the `CustomerSupportIntegrations` inline IAM policy. That policy covers KB retrieval, Memory, and Browser. Model invocation and Code Interpreter permissions are separate checks.

Deployment, IAM apply, agent invocation, refund tools, and memory event creation were not run for repository preparation. Examples in documentation are future authorized procedures. No infrastructure-as-code stack or new AWS resource configuration was added.

## Evidence and production boundaries

The final [evidence index](../evidence/README.md) includes 13 genuine PNGs: eight unchanged historical captures and five current hosted screenshots. Current images verify order command/response, fresh-actor Memory with different application and Runtime IDs, all eight displayed loyalty JSON values and READY Runtime version 2. The accepted Refund, RAG and Browser captures and 285-word reflection are preserved without unnecessary live retesting. Earlier failed Memory and contradictory $15 loyalty wording remain in the historical audit trail.

Screenshot 14 records the October 28 deployment update and artifact location. Anonymous read-only HEAD access to that precise S3 object returned 403, so the deployed source archive could not be compared. The local source digest matches the screenshot but is not a deployed-source fingerprint. Current loyalty screenshot 13 is an agent JSON response, not a raw sandbox event. Raw remote Code Interpreter execution remains unverified at the service-trace level; source and executed offline output independently verify the structured tool result.

## Attempt 2 result contract

The reviewer required `tier_discount_pct`, missing from the original seven-field result. The corrected source returns fractional 0.00, 0.10 or 0.15, with unknown tiers using 0.00. It still invokes executeCode/clearContext and reads the first result event, but extracts business JSON from stdout/text rather than returning only the SDK envelope. Missing fields, execution errors, missing events and unavailable service use explicit eight-field tier-only fallback with no points redeemed/earned.

[The final actual offline log](../evidence/16_offline_verification_2026-10-29.txt) records 35 passing cases and the direct structured calculator output. Generated Python really runs locally through a mocked Code Interpreter dependency. [Screenshot 13](../evidence/13_loyalty.png) independently shows the matching hosted agent JSON; neither item is misrepresented as a raw AWS tool event. See the [AWS result API](https://docs.aws.amazon.com/bedrock-agentcore/latest/APIReference/API_CodeInterpreterResult.html) and [invoke response](https://docs.aws.amazon.com/bedrock-agentcore/latest/APIReference/API_InvokeCodeInterpreter.html) for the referenced interfaces.
