# AI Support Agent with Amazon Bedrock AgentCore and Strands SDK

**Model-driven support workflows with MCP tools, grounded answers, and customer memory.**

[![AWS: AgentCore](https://img.shields.io/badge/AWS-AgentCore-232F3E)](https://aws.amazon.com/bedrock/agentcore/)
[![Amazon Bedrock: Nova 2 Lite](https://img.shields.io/badge/Amazon_Bedrock-Nova_2_Lite-FF9900)](https://aws.amazon.com/bedrock/)
[![Python: 3.13](https://img.shields.io/badge/Python-3.13-3776AB)](starter/pyproject.toml)
[![Strands: Agents SDK](https://img.shields.io/badge/Strands-Agents_SDK-6C47FF)](https://strandsagents.com/)
[![MCP: Streamable HTTP](https://img.shields.io/badge/MCP-Streamable_HTTP-111827)](docs/ARCHITECTURE.md)
[![Udacity: Project 2](https://img.shields.io/badge/Udacity-Project_2-02B3E4)](docs/UDACITY_ATTRIBUTION.md)

A Python agent for a fictional e-commerce store that can look up orders, simulate refunds, retrieve product and policy information, remember preferences, calculate loyalty discounts, and browse live webpages. Amazon Nova 2 Lite selects the tools; Strands runs the agent loop; Amazon Bedrock AgentCore provides the hosted runtime and managed integrations.

Completed for **Project 2 of the Udacity AWS AI & ML Nanodegree**. This project is separate from the earlier customer-support chatbot.

> **Private educational repository.** Order/customer records are fixtures and refunds are simulations. AWS infrastructure must be configured separately. Screenshot evidence is **PENDING**; the author will add the actual captures. See [licensing](docs/UDACITY_ATTRIBUTION.md) before sharing or changing visibility.

[Architecture](docs/ARCHITECTURE.md) · [Detailed setup](starter/README.md) · [Engineering notes](docs/TECHNICAL_DETAILS.md) · [Reflection](REFLECTION.md) · [Evidence](evidence/README.md) · [Submission checklist](docs/SUBMISSION_CHECKLIST.md)

## Project overview

The engineering focus is the boundary between language-model reasoning and concrete tool contracts. Order retrieval uses a REST proxy integration, refunds use direct Lambda tool arguments, Knowledge Base retrieval returns passages, and memory hooks add customer context before the agent reasons. Each capability has its own failure modes and permissions.

The implementation keeps those boundaries visible: one Runtime entry point, MCP tool discovery, explicit memory hooks, a retrieval tool, a remote computation tool with a reduced fallback, and a managed browser integration. The working Python source and dependency files are preserved from the completed project.

## Six core capabilities

| Capability | Example customer request | Implementation |
| --- | --- | --- |
| Order tracking | “Can you track order ORD-001?” | MCP Gateway → API Gateway → order Lambda |
| Simulated refunds | “Please refund my Kindle order ORD-002.” | MCP Gateway → refund Lambda |
| Grounded answers | “What are the Platinum tier benefits?” | Knowledge Base `Retrieve` → Nova response |
| Cross-session recall | “Do you remember my communication preference?” | Semantic/user-preference records via `MemoryHook` |
| Loyalty calculation | “Apply my 4,250 Gold points to a $150 standard order.” | Code Interpreter tool with a tier-only fallback |
| Live web retrieval | “Visit Udacity and tell me the page title.” | Strands browser tool → AgentCore Browser |

## Technology stack

| Layer | Technologies |
| --- | --- |
| Language and dependencies | Python 3.13, uv, `pyproject.toml`, `uv.lock` |
| Reasoning and orchestration | Amazon Nova 2 Lite (`global.amazon.nova-2-lite-v1:0`), Strands Agents SDK |
| Hosting and tool protocol | AgentCore Runtime, AgentCore Gateway, MCP Streamable HTTP |
| Business tools | Amazon API Gateway REST API, two AWS Lambda handlers |
| Retrieval and storage | Amazon Bedrock Knowledge Base, Amazon S3 catalog source |
| Context and managed tools | AgentCore Memory, Code Interpreter, Browser |
| Access and operations | AWS IAM, CloudWatch execution logs, Boto3 |

Resolved package versions and the Python Starter Toolkit compatibility notes are documented in [starter/README.md](starter/README.md#technology-stack).

## AWS architecture

```mermaid
flowchart TD
    CUSTOMER["Customer request"] --> RUNTIME["AgentCore Runtime: HTTP entry point"]
    RUNTIME --> AGENT["Strands Agent in main.py"]
    AGENT <--> NOVA["Amazon Bedrock: Nova 2 Lite"]

    AGENT --> MCP["MCPClient: tool discovery and calls"]
    MCP --> GATEWAY["AgentCore Gateway"]
    GATEWAY --> API["API Gateway REST target"]
    API --> ORDERS["Order Tracking Lambda"]
    GATEWAY --> REFUNDS["Refund Lambda: simulated operations"]

    AGENT --> RAG["RAG retrieval tool"]
    RAG --> KB["Bedrock Knowledge Base: Retrieve"]
    S3["S3: product_catalog.txt"] -.->|"configured ingestion"| KB

    AGENT --> HOOK["MemoryHook"]
    HOOK <--> MEMORY["AgentCore Memory: facts and preferences"]
    AGENT --> LOYALTY["Loyalty calculation tool"]
    LOYALTY --> CODE["AgentCore Code Interpreter"]
    LOYALTY -.->|"on failure"| FALLBACK["Tier-only local fallback"]
    AGENT --> TOOL["Strands browser tool"]
    TOOL --> BROWSER["AgentCore Browser"]

    IAM["IAM execution and service roles"] -.-> RUNTIME
    IAM -.-> GATEWAY
    RUNTIME -.-> LOGS["CloudWatch execution logs"]
    ORDERS -.-> LOGS
    REFUNDS -.-> LOGS
```

The same handler can run in a local HTTP process. S3 ingestion and AWS service configuration are external setup, not automatic provisioning by `main.py`. The application does not fetch the catalog from S3 on every request. See [architecture boundaries](docs/ARCHITECTURE.md) for event contracts and trust boundaries.

## How a request is processed

1. A module-level `BedrockAgentCoreApp` receives a JSON payload with `prompt`, `customer_id`, and `session_id`.
2. The handler validates the prompt and generates UUIDs for missing actor/session IDs.
3. It constructs `MemoryHook` and Browser, connects to Gateway, and discovers MCP tools with `list_tools_sync()`.
4. A fresh Strands `Agent` receives those tools, the Knowledge Base and loyalty tools, and the Nova model.
5. The memory hook retrieves relevant stored records; Nova selects tools and composes the answer.
6. The completed user/assistant turn is saved as a memory event. The handler returns text from the first assistant content block.

Each invocation constructs a new agent. Saved events do not imply that a complete prior conversation is automatically replayed.

### MCP Gateway and business tools

The order handler expects API Gateway proxy events for `GET /orders/{order_id}`, `GET /customers/{customer_id}/orders`, and `GET /customers/{customer_id}`. The refund handler receives direct tool arguments and dispatches using `bedrockAgentCoreToolName` in Lambda client context.

The refund [schema](starter/lambda/lambda_schema) exposes `initiate_refund`, `check_refund_status`, and `get_return_label`. Refund IDs and return labels are simulated; there is no payment processor or persistent refund database. [Integration details](starter/README.md#gateway-tools-and-workflows).

### RAG and Knowledge Base retrieval

`search_knowledge_base()` calls the Bedrock Knowledge Base **Retrieve** API and returns text chunks to Nova. The educational [catalog](starter/product_catalog.txt) supplies products, policy rules, and loyalty information after separate S3 ingestion. The implementation does not return structured retrieval citations. [RAG details](starter/README.md#knowledge-base-rag).

### Cross-session memory

`MemoryHook` searches the configured semantic and user-preference namespaces before reasoning and saves each completed turn afterward. Recall requires a stable customer ID and asynchronous extraction. The reported cross-session test succeeded after retry. The application does not restore raw session history across requests. [Memory details](starter/README.md#short-term-and-long-term-memory).

### Code Interpreter and loyalty arithmetic

The tool sends Python using `Decimal` to AgentCore Code Interpreter. It redeems whole 500-point blocks, caps points redemption at 50% of order value, then applies the tier discount and awards new points.

For 4,250 points, Gold tier, and a $150 standard order, the expected complete breakdown is **4,000 points redeemed, $40 points discount, $11 tier discount, $99 final total, $51 savings, 99 points earned, and 349 remaining points**.

A failure returns a reduced, explicitly marked tier-only calculation. A correct final number alone does not independently prove that remote sandbox execution occurred. [Calculation and fallback](starter/README.md#loyalty-discount-computation).

### AgentCore Browser

The registered `AgentCoreBrowser.browser` tool supports live webpage access. The reported browser scenario retrieved a live page successfully. Page content changes over time; there is no hardcoded expected title or fabricated screenshot. [Browser details](starter/README.md#agentcore-browser).

## Verified functional tests

These results were reported by the project author. Documentation preparation used offline checks and did not rerun live agent or AWS tool operations.

| Local scenario | Reported outcome | Screenshot evidence |
| --- | --- | --- |
| Order tracking | Successful | PENDING |
| Simulated refund processing | Successful | PENDING |
| Knowledge Base RAG | Successful | PENDING |
| Cross-session memory | Successful after retry | PENDING |
| Loyalty discount | Correct complete numerical breakdown | PENDING |
| Browser retrieval | Successful live webpage retrieval | PENDING |

Runbooks and expected outcomes are in the [six local scenarios](starter/README.md#six-verified-local-scenarios). Screenshot requirements and filenames are in [evidence/README.md](evidence/README.md). Independent Code Interpreter execution evidence remains unverified.

## Successful cloud deployment

The author reports that AgentCore Runtime reached **READY** and successfully answered an order-tracking request for **ORD-001**. The original local deployment metadata and Linux ARM64 dependency package were inspected during preparation; private configuration and generated artifacts are intentionally excluded from this repository.

Deployment and cloud-invocation screenshots are **PENDING**. The six local results are not represented as six independently repeated cloud Runtime tests. No deployment or cloud re-invocation was performed to prepare this repository.

## Installation and configuration

Prerequisites: Python 3.13, uv, AWS CLI v2, authorized AWS credentials, and the separately configured AWS integrations. Cloning alone does not provision them.

```bash
git clone https://github.com/Hatch5t/aws-ai-support-agent-strands-agentcore.git
cd aws-ai-support-agent-strands-agentcore/starter
uv sync --python 3.13 --locked
```

Use the existing Python Starter Toolkit environment. The installed toolkit version is deprecated; its commands differ from the newer npm AgentCore CLI. Avoid mixing executables. See the [compatibility explanation](starter/README.md#prerequisites-and-local-installation).

The unchanged `main.py` uses module-level `GATEWAY_URL`, `KB_ID`, `REGION`, and `MEMORY_ID` constants. It already contains account-specific settings. These are not environment-variable overrides, and no `.env` loader is implemented. Credentials must remain external to Git. See [AWS configuration](starter/README.md#aws-configuration) for temporary-profile guidance and illustrative resource placeholders.

The educational client opens an unsigned Gateway connection. This private copy preserves that implementation; securing it and removing embedded endpoint identifiers requires a separate authorized source change before broader sharing or production use.

## Local testing

From `starter/`, start the saved HTTP entry point:

```bash
uv run --locked main.py
```

In another terminal:

```bash
curl --fail-with-body -X POST http://localhost:8080/invocations \
  -H 'Content-Type: application/json' \
  -d '{"prompt":"Can you track order ORD-001?","customer_id":"CUST-123","session_id":"local-order-1"}'
```

The payload is the direct JSON object. The top-of-file JSON CLI example refers to a dormant helper; `app.run()` starts the server in the saved version. Local requests still call AWS and may write memory events. [Full local test instructions](starter/README.md#local-invocation).

## Deployment instructions

The following is a reproduction procedure for an authorized deployment, not a request to redeploy the completed project:

```bash
# From starter/, using the Python Starter Toolkit CLI
uv run --locked agentcore configure \
  --entrypoint main.py \
  --name CustomerSupportAgent \
  --region us-east-1 \
  --deployment-type direct_code_deploy \
  --runtime PYTHON_3_13 \
  --requirements-file pyproject.toml \
  --disable-memory

uv run --locked agentcore deploy
```

Direct Code Deploy packages Python and Linux ARM64 dependencies for Runtime. `--disable-memory` disables toolkit-created memory, not the explicit application `MemoryHook`. Inspect existing settings before reconfiguring any deployed agent.

The existing `setup_permissions.py` helper has a no-AWS-call `--dry-run` option. Running it without that flag **changes IAM**, and it grants KB, Memory, and Browser actions rather than all integration permissions. Read the [complete deployment and permissions procedure](starter/README.md#agentcore-runtime-deployment) before any future deployment.

## Engineering challenges and lessons

| Challenge | Implemented response / lesson |
| --- | --- |
| Python 3.13 / Linux ARM64 native dependency compatibility | Pin `lazy-object-proxy==1.12.0`; the lockfile and original archive contain compatible artifacts |
| Memory extraction delay | Allow asynchronous extraction; cross-session recall succeeded after retry |
| Different tool event contracts | Keep API Gateway proxy routing distinct from direct Gateway Lambda arguments |
| Retrieved context leaking into saved queries | Preserve the original user text before memory-context injection |
| Remote calculation availability | Return an explicit tier-only fallback and distinguish it from complete results |
| Reproducibility across environments | Local `uv sync --locked` preserves the lock; the inspected toolkit's deployment resolver is not proven to freeze all transitive dependencies |

Read the [reflection](REFLECTION.md) and [technical notes](docs/TECHNICAL_DETAILS.md) for the design rationale and evidence boundaries.

## Security considerations and known limitations

- **Access boundaries:** the Gateway client is unsigned, customer IDs are caller-controlled, and tool consent is bypassed for headless execution. Production needs authenticated identities, secure Gateway access, ownership checks, and explicit controls for state-changing operations.
- **Data protection:** memory and logs can retain prompts or tool payloads. Define access restrictions, encryption, retention, deletion, and customer-memory isolation. Both Lambda handlers currently log incoming events.
- **Repository hygiene:** credentials, environment files, private deployment settings, logs, and dependency archives are excluded. The unchanged source retains resource identifiers; private visibility is essential and does not make the service secure.
- **Application limits:** business data is mocked, refund state is not durable, KB citations are not rendered, raw conversation history is not replayed, and Gateway discovery is required per invocation.
- **Verification limits:** screenshots are pending, all-six cloud coverage is not established, sandbox execution is not independently verified, and no load test, penetration test, or production-readiness certification is claimed.

See the [validation record](docs/VALIDATION.md), [full security discussion](starter/README.md#security-and-production-considerations), and [limitations](starter/README.md#known-limitations).

## Repository guide

| Location | Purpose |
| --- | --- |
| [starter/README.md](starter/README.md) | Detailed implementation, installation, configuration, and test runbooks |
| [starter/main.py](starter/main.py) | Completed agent with original instructional comments retained |
| [starter/lambda/](starter/lambda/) | Order/refund Lambda handlers and refund tool schema |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Service paths, event contracts, and trust boundaries |
| [docs/TECHNICAL_DETAILS.md](docs/TECHNICAL_DETAILS.md) | Lifecycle, arithmetic, memory, packaging, and operational notes |
| [REFLECTION.md](REFLECTION.md) | 200–400 word project reflection |
| [docs/SUBMISSION_CHECKLIST.md](docs/SUBMISSION_CHECKLIST.md) | Source mapping and pending reviewer evidence |
| [evidence/README.md](evidence/README.md) | Eight screenshot slots; no fabricated images |
| [docs/upstream/UDACITY_PROJECT_INSTRUCTIONS.md](docs/upstream/UDACITY_PROJECT_INSTRUCTIONS.md) | Original upstream README preserved verbatim |

## Udacity attribution and author

Built by **[Aarush Rajan Ranjan / Hatch5t](https://github.com/Hatch5t)** for Udacity Nanodegree Project 2, based on the [Udacity AgentCore starter](https://github.com/udacity/cd14763-project-starter). AWS, Strands, and other product names identify technologies used; no endorsement is implied.

The original [LICENSE.txt](LICENSE.txt) is unchanged. It contains educational-content restrictions referencing CC BY-NC-ND and a 3.0/4.0 version inconsistency. No replacement open-source license is applied. Keep this repository private; public redistribution and sharing of modified starter content require clarification. [Full attribution and licensing notes](docs/UDACITY_ATTRIBUTION.md).
