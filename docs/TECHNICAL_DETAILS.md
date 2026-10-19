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

The handler discovers Gateway tools before reasoning. Gateway failure therefore prevents unrelated KB or browser requests from reaching the agent. It returns only the first assistant content block's text, and a caught exception returns a generic text error. Test response content and tool traces rather than relying on HTTP status alone.

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
| Complete output | Redeemed points, points/tier discounts, final total, savings, earned/remaining points |
| Error path | Local floating-point tier discount only, `fallback: true` |

For the reported Gold / 4,250 points / $150 standard order: redeem 4,000 points, subtract $40, apply $11 tier discount, pay $99, save $51, earn 99 points, and finish with 349 points. This expected result is a calculation contract, not independent evidence that `executeCode` ran remotely.

## Python 3.13 and Linux ARM64

The manifest pins `lazy-object-proxy==1.12.0`; the lockfile includes a CPython 3.13 ARM64 Linux wheel. The original local dependency ZIP was previously inspected and contained its matching Linux ARM64 extension. That ZIP is excluded from this repository.

The author identifies native dependency compatibility as the deployment failure that required resolution. The exact earlier failing version/error transcript is unavailable, so it is not reconstructed here. A local macOS install is insufficient proof of target compatibility.

The Python Starter Toolkit is locked to `0.3.14`, and its installed help warns that it is deprecated. Reproduction uses that project's Python CLI, not the newer npm CLI project format. The inspected packager compiles manifest requirements and installs binary-only packages for Linux ARM64. It hashes `uv.lock` for cache invalidation but does not establish frozen transitive resolution during deployment. Local `uv sync --locked` and deployment packaging must therefore be evaluated separately.

## Permissions and state changes

The helper's `--dry-run` reads local files and prints a policy without AWS calls. Its normal mode validates account/role/resource consistency and writes the `CustomerSupportIntegrations` inline IAM policy. That policy covers KB retrieval, Memory, and Browser. Model invocation and Code Interpreter permissions are separate checks.

Deployment, IAM apply, agent invocation, refund tools, and memory event creation were not run for repository preparation. Examples in documentation are future authorized procedures. No infrastructure-as-code stack or new AWS resource configuration was added.

## Evidence and production boundaries

All eight [screenshots](../evidence/README.md) are present, readable, and reviewed: six local scenarios, successful deployment, and one hosted order invocation. Screenshot 05 verifies the calculator call and complete numbers without independently proving sandbox execution. Screenshot 06 shows browser-tool retrieval from example.com; its Safari window is separate. Screenshot 07 includes a trace-delivery warning, so observability is not fully verified. Full six-scenario cloud repetition, sandbox execution, concurrency/load behavior, and security hardening remain unverified. The [code-level audit](RUBRIC_AUDIT.md) maps the supplied A–G criteria; the separate official classroom rubric was unavailable.
