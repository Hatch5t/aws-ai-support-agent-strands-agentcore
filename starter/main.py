"""
Customer Support AI Agent — Starter Code
==========================================
Your task is to complete this file by implementing all sections marked
with # TODO comments.

Reference the project instructions and rubric for guidance.
Work through each section yourself.

Run locally (after filling in config values):
  uv run main.py '{"prompt": "Hello", "customer_id": "CUST-123", "session_id": "s1"}'

Deploy to AgentCore:
  agentcore deploy

Invoke deployed agent:
  agentcore invoke '{"prompt": "Hello", "customer_id": "CUST-123", "session_id": "s1"}'
"""

# ── Imports ───────────────────────────────────────────────────────────────────
# These imports are provided. Do not remove them.
from strands import Agent, tool
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from bedrock_agentcore.memory import MemoryClient
from strands.models import BedrockModel
from strands.tools.mcp.mcp_client import MCPClient
from mcp.client.streamable_http import streamable_http_client
from contextlib import ExitStack, contextmanager
import argparse, json
import os, asyncio, boto3
from strands.hooks import (
    HookProvider, AfterInvocationEvent, HookRegistry, MessageAddedEvent,
)
import logging
import uuid
from typing import Dict
from bedrock_agentcore.tools.code_interpreter_client import code_session
from strands_tools.browser import AgentCoreBrowser


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("CSAI_Agent")
logger.setLevel(logging.INFO)

# ── TODO 1 — App Initialisation ───────────────────────────────────────────────
# Create a BedrockAgentCoreApp instance.
# This registers the ASGI server for AgentCore deployment.
# There must be exactly one instance per deployment.
#
# Hint: app = BedrockAgentCoreApp()

# TODO: Create the BedrockAgentCoreApp instance
app = BedrockAgentCoreApp()  # Replace this line


# Suppress interactive tool-consent prompts (required in headless deployments).
os.environ["BYPASS_TOOL_CONSENT"] = "true"


# ── TODO 2 — Configuration ────────────────────────────────────────────────────
# Replace the placeholder strings with your actual AWS resource values.
# You collected these in the infrastructure setup section of the project instructions.
#
# GATEWAY_URL format: https://<alias>.gateway.bedrock-agentcore.<region>.amazonaws.com/mcp
# This starter uses an unsigned MCP connection and therefore assumes the
# project Gateway is configured with the NONE authorizer.
# KB_ID       format: 10-character alphanumeric string from the KB console
# REGION:     your AWS region, e.g. "us-east-1"
# MEMORY_ID   format: shown in the AgentCore Memory console

GATEWAY_URL = "https://customersupportgateway-eiplzymrzt.gateway.bedrock-agentcore.us-east-1.amazonaws.com/mcp"   # TODO: Replace with your Gateway URL
KB_ID       = "P1IM05S1VK"          # TODO: Replace with your Knowledge Base ID
REGION      = "us-east-1"        # TODO: Replace with your AWS region
MEMORY_ID   = "CustomerSupportMemory-oOfSADE4Vx"        # TODO: Replace with your Memory ID


# ── TODO 3 — Model and Clients ────────────────────────────────────────────────
# Create:
#   1. A BedrockModel using model_id "global.amazon.nova-2-lite-v1:0"
#   2. A MemoryClient with region_name=REGION
#   3. A boto3 client for the "bedrock-agent-runtime" service in REGION
#
# Hint: model = BedrockModel(model_id=model_id)

model_id = "global.amazon.nova-2-lite-v1:0"

# TODO: Create the BedrockModel instance
model = BedrockModel(
    model_id=model_id,
    region_name=REGION
)  # Replace this line

# TODO: Create the MemoryClient instance
memory_client = MemoryClient(
    region_name=REGION
)  # Replace this line

# TODO: Create the boto3 bedrock-agent-runtime client
_bedrock_runtime = boto3.client(
    "bedrock-agent-runtime",
    region_name=REGION
) # Replace this line


# ── TODO 4 — Namespace Helper ─────────────────────────────────────────────────
# Implement get_namespaces() to return a dict mapping strategy type to
# namespace template string.
#
# Steps:
#   1. Call mem_client.get_memory_strategies(memory_id) to get strategy list
#   2. Read the namespace from strategy["namespaceTemplates"][0].
#      For compatibility with older AgentCore responses, fall back to
#      strategy["namespaces"][0] when namespaceTemplates is absent.
#
# Example output:
#   { "SEMANTIC": "cs_agent/{actorId}/facts",
#     "USER_PREFERENCE": "cs_agent/{actorId}/preferences" }

def get_namespaces(mem_client: MemoryClient, memory_id: str) -> Dict:
    """Return a dict mapping strategy type to namespace template."""

    strategies = mem_client.get_memory_strategies(memory_id)

    namespaces = {}

    for strategy in strategies:
        strategy_type = strategy["type"]

        templates = (
            strategy.get("namespaceTemplates")
            or strategy.get("namespaces")
            or []
        )

        if templates:
            namespaces[strategy_type] = templates[0]

    return namespaces

# ── TODO 5 — Memory Hook ──────────────────────────────────────────────────────
# Implement MemoryHook, a HookProvider subclass that adds long-term memory.
#
# The class needs:
#   __init__(self, actor_id, session_id, memory_client, memory_id)
#     — store all four as instance attributes
#     — call get_namespaces() and store the result as self.namespaces
#
#   retrieve_customer_context(self, event: MessageAddedEvent)
#     — only runs for plain-text user messages (not tool results)
#     — for each strategy namespace, call memory_client.retrieve_memories(
#          memory_id, namespace (formatted with actorId), query, top_k=5)
#     — collect non-empty memory texts tagged with their strategy type
#     — if any memories found, prepend them to the user message as:
#          "Customer Context:\n<memories>\n\n<original_message>"
#
#   save_support_interaction(self, event: AfterInvocationEvent)
#     — walk the message list backwards to find the last plain-text user
#       query and the last assistant response
#     — call memory_client.create_event(memory_id, actor_id, session_id,
#          messages=[(customer_query, "USER"), (agent_response, "ASSISTANT")])
#
#   register_hooks(self, registry: HookRegistry)
#     — register retrieve_customer_context on MessageAddedEvent
#     — register save_support_interaction on AfterInvocationEvent

class MemoryHook(HookProvider):
    """Long-term memory hook for the customer support agent."""

    def __init__(
        self,
        actor_id: str,
        session_id: str,
        memory_client: MemoryClient,
        memory_id: str,
    ):
        # TODO: Store actor_id, session_id, memory_id, memory_client as attributes
        # TODO: Call get_namespaces() and store the result as self.namespaces
        self.actor_id = actor_id
        self.session_id = session_id
        self.memory_client = memory_client
        self.memory_id = memory_id
        self.namespaces = get_namespaces(memory_client, memory_id)
        self._original_user_query = None

    def retrieve_customer_context(self, event: MessageAddedEvent):
        """Retrieve relevant memories and prepend them to the user message."""
        # TODO: Implement memory retrieval
        # Steps:
        #   1. Get the last message from event.agent.messages
        #   2. Check it is a user message and not a tool result
        #   3. Extract the user query text
        #   4. For each namespace in self.namespaces, call retrieve_memories()
        #   5. Collect non-empty memory texts with strategy type tags
        #   6. If any found, prepend them to the user message
        messages = event.agent.messages
        if not messages:
            return

        message = messages[-1]
        if message.get("role") != "user":
            return

        blocks = message.get("content", [])

        # Only process plain-text messages, not tool results.
        if (
            len(blocks) != 1
            or not isinstance(blocks[0], dict)
            or not isinstance(blocks[0].get("text"), str)
        ):
            return

        original_text = blocks[0]["text"]
        if not original_text.strip():
            return

        # Preserve the actual customer message for saving later.
        self._original_user_query = original_text

        all_context = []

        for strategy_type, template in self.namespaces.items():
            try:
                namespace = template.format(
                    actorId=self.actor_id,
                    sessionId=self.session_id,
                )

                memories = self.memory_client.retrieve_memories(
                    memory_id=self.memory_id,
                    namespace=namespace,
                    query=original_text,
                    top_k=5,
                )

                for memory in memories:
                    content = memory.get("content", {})
                    text = content.get("text", "").strip()

                    if text:
                        all_context.append(
                            f"[{strategy_type}] {text}"
                        )

            except Exception:
                logger.exception(
                    "Failed to retrieve %s memories",
                    strategy_type,
                )

        if all_context:
            context_text = "\n".join(all_context)
            blocks[0]["text"] = (
                f"Customer Context:\n{context_text}"
                f"\n\n{original_text}"
            )

    def save_support_interaction(self, event: AfterInvocationEvent):
        """Save the completed turn to memory after the agent responds."""
        # TODO: Implement memory saving
        # Steps:
        #   1. Get messages from event.agent.messages
        #   2. Walk backwards to find the last user query (plain text)
        #      and the last assistant response
        #   3. Call memory_client.create_event() with both messages
        messages = event.agent.messages
        customer_query = self._original_user_query
        agent_response = None

        for message in reversed(messages):
            role = message.get("role")
            blocks = message.get("content", [])

            if any(
                isinstance(block, dict) and "toolResult" in block
                for block in blocks
            ):
                continue

            texts = [
                block["text"]
                for block in blocks
                if isinstance(block, dict)
                and isinstance(block.get("text"), str)
                and block["text"].strip()
            ]

            if not texts:
                continue

            if role == "assistant" and agent_response is None:
                agent_response = "\n".join(texts)

            elif role == "user" and customer_query is None:
                customer_query = "\n".join(texts)

            if customer_query and agent_response:
                break

        if customer_query and agent_response:
            try:
                self.memory_client.create_event(
                    memory_id=self.memory_id,
                    actor_id=self.actor_id,
                    session_id=self.session_id,
                    messages=[
                        (customer_query, "USER"),
                        (agent_response, "ASSISTANT"),
                    ],
                )
                logger.info("Customer interaction saved to memory")

            except Exception:
                logger.exception("Failed to save customer interaction")

    def register_hooks(self, registry: HookRegistry) -> None:  # type: ignore
        """Register both memory callbacks."""
        # TODO: Register retrieve_customer_context on MessageAddedEvent
        # TODO: Register save_support_interaction on AfterInvocationEvent
        registry.add_callback(
            MessageAddedEvent,
            self.retrieve_customer_context,
        )

        registry.add_callback(
            AfterInvocationEvent,
            self.save_support_interaction,
        )



# ── TODO 6 — Knowledge Base Tool ─────────────────────────────────────────────
# Implement search_knowledge_base(query) using the @tool decorator.
#
# Steps:
#   1. Guard: if KB_ID is empty return "Knowledge base not configured."
#   2. Call _bedrock_runtime.retrieve(
#          knowledgeBaseId=KB_ID,
#          retrievalQuery={"text": query}
#      )
#   3. Extract resp["retrievalResults"]; return a message if empty
#   4. Join the text chunks with "\n---\n" and return the result
#
# The docstring is the tool description — the model uses it to decide when
# to call this tool, so keep it clear and accurate.

@tool
def search_knowledge_base(query: str) -> str:
    """
    Search the Amazon product catalog and support knowledge base.
    Use this for product specifications, return policies, warranty
    information, loyalty program details, and order status definitions.

    Args:
        query: The question or topic to search for

    Returns:
        Relevant information retrieved from the knowledge base
    """
    # TODO: Implement the Knowledge Base search
    if not KB_ID or KB_ID.startswith("<"):
        return "Knowledge base not configured."

    response = _bedrock_runtime.retrieve(
        knowledgeBaseId=KB_ID,
        retrievalQuery={"text": query},
    )

    results = response.get("retrievalResults", [])

    if not results:
        return "No relevant knowledge base results found."

    return "\n---\n".join(
        result.get("content", {}).get("text", "")
        for result in results
        if result.get("content", {}).get("text")
    )


# ── TODO 7 — Loyalty Discount Tool (Code Interpreter) ────────────────────────
# Implement calculate_loyalty_discount() using the @tool decorator.
#
# The tool must:
#   1. Build a self-contained Python code string that:
#        • Defines earn_rates: {"standard": 1, "device": 2, "fresh": 5}
#        • Defines tier_rates: {"Silver": 0.00, "Gold": 0.10, "Platinum": 0.15}
#        • Calculates points_redeemed (floor to nearest 500, cap at 50% of order)
#        • Calculates tier_discount (applied to subtotal after points)
#        • Calculates final_total, total_savings, points_earned, remaining_points
#        • Prints a JSON result dict
#   2. Execute the code with code_session(REGION).invoke("executeCode", {...})
#      using language="python" and clearContext=True
#   3. Return the first result event as a JSON string
#   4. Include a fallback that computes only the tier discount if the
#      Code Interpreter is unavailable

@tool
def calculate_loyalty_discount(
    loyalty_points: int,
    tier: str,
    order_total: float,
    product_category: str = "standard",
) -> str:
    """
    Calculate the loyalty discount for a customer order using the
    AgentCore Code Interpreter. Runs exact arithmetic in a secure sandbox.

    Args:
        loyalty_points:   Customer's current points balance
        tier:             Customer tier — Silver, Gold, or Platinum
        order_total:      Order total in USD
        product_category: standard, device, or fresh

    Returns:
        Full discount breakdown and final price
    """
    # TODO: Build the code string (use an f-string to inject the arguments)
    code = f'''
import json
from decimal import Decimal, ROUND_HALF_UP

loyalty_points = max(0, int({loyalty_points!r}))
tier = {tier!r}
order_total = max(Decimal("0"), Decimal(str({order_total!r})))
product_category = {product_category!r}

earn_rates = {{"standard": 1, "device": 2, "fresh": 5}}
tier_rates = {{
    "Silver": Decimal("0.00"),
    "Gold": Decimal("0.10"),
    "Platinum": Decimal("0.15")
}}

point_value = Decimal("0.01")

available_points = (loyalty_points // 500) * 500

max_points = int(
    ((order_total * Decimal("0.50")) / point_value) // 500
) * 500

points_redeemed = min(available_points, max_points)

points_discount = Decimal(points_redeemed) * point_value

subtotal = order_total - points_discount

tier_discount = (
    subtotal * tier_rates.get(tier, Decimal("0.00"))
).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

final_total = (
    subtotal - tier_discount
).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

total_savings = (
    points_discount + tier_discount
).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

points_earned = int(
    final_total * earn_rates.get(product_category, 1)
)

remaining_points = (
    loyalty_points - points_redeemed + points_earned
)

result = {{
    "points_redeemed": points_redeemed,
    "points_discount": float(points_discount),
    "tier_discount_pct": float(tier_rates.get(tier, Decimal("0.00"))),
    "tier_discount": float(tier_discount),
    "final_total": float(final_total),
    "total_savings": float(total_savings),
    "points_earned": points_earned,
    "remaining_points": remaining_points
}}

print(json.dumps(result))
'''  # Replace with your code string


    try:
        # TODO: Execute the code using code_session and return the result
        with code_session(REGION) as client:
            response = client.invoke(
                "executeCode",
                {
                    "code": code,
                    "language": "python",
                    "clearContext": True
                }
            )

            for event in response["stream"]:
                if "result" in event:
                    result = event["result"]

                    if result.get("isError"):
                        raise RuntimeError(
                            "Code Interpreter execution failed"
                        )

                    # Return business fields rather than only the SDK envelope.
                    structured = result.get("structuredContent") or {}
                    if structured.get("exitCode", 0) != 0:
                        raise RuntimeError("Code Interpreter returned a nonzero exit code")

                    outputs = [structured.get("stdout", "")]
                    outputs.extend(
                        block.get("text", "")
                        for block in result.get("content", [])
                        if block.get("type") == "text"
                    )
                    required = {
                        "points_redeemed", "points_discount", "tier_discount_pct",
                        "tier_discount", "final_total", "total_savings",
                        "points_earned", "remaining_points",
                    }
                    for output in outputs:
                        try:
                            breakdown = json.loads(output)
                        except (TypeError, ValueError):
                            continue
                        if isinstance(breakdown, dict) and required <= breakdown.keys():
                            return json.dumps(breakdown)

                    raise RuntimeError("Code Interpreter returned no complete loyalty result")

            raise RuntimeError(
                "Code Interpreter returned no result"
            )


    except Exception:
        logger.exception("Code Interpreter unavailable; using tier-only fallback")
        # TODO: Implement fallback calculation using tier discount only
        tier_rates = {
            "Silver": 0.00,
            "Gold": 0.10,
            "Platinum": 0.15
        }

        tier_discount = round(
            order_total * tier_rates.get(tier, 0.00),
            2
        )

        final_total = round(
            order_total - tier_discount,
            2
        )

        return json.dumps({
            "points_redeemed": 0,
            "points_discount": 0.0,
            "tier_discount_pct": tier_rates.get(tier, 0.00),
            "tier_discount": tier_discount,
            "final_total": final_total,
            "total_savings": tier_discount,
            "points_earned": 0,
            "remaining_points": max(0, int(loyalty_points)),
            "fallback": True,
            "message": (
                "Code Interpreter unavailable. Tier discount only; "
                "points were not redeemed or earned."
            ),
        })


GATEWAY_UNAVAILABLE_MESSAGE = (
    "The order and refund services are temporarily unavailable. "
    "Please try again later."
)


class GatewayUnavailableError(RuntimeError):
    """Gateway setup or cleanup failed; callers receive a safe service message."""


@contextmanager
def gateway_tool_session():
    """Discover tools and keep the MCP connection open for agent execution."""
    stack = ExitStack()
    try:
        try:
            mcp_client = stack.enter_context(MCPClient(
                lambda: streamable_http_client(GATEWAY_URL)
            ))
            gateway_tools = mcp_client.list_tools_sync()
        except TimeoutError as error:
            logger.exception("Gateway connection or tool discovery timed out")
            raise GatewayUnavailableError(GATEWAY_UNAVAILABLE_MESSAGE) from error
        except ConnectionError as error:
            logger.exception("Gateway connection or tool discovery failed")
            raise GatewayUnavailableError(GATEWAY_UNAVAILABLE_MESSAGE) from error
        except Exception as error:
            logger.exception("Unexpected Gateway connection or discovery failure")
            raise GatewayUnavailableError(GATEWAY_UNAVAILABLE_MESSAGE) from error

        if not gateway_tools:
            logger.warning("Gateway discovery returned no tools")
            raise GatewayUnavailableError(GATEWAY_UNAVAILABLE_MESSAGE)

        logger.info("Discovered %d Gateway tools", len(gateway_tools))
        yield gateway_tools
    finally:
        try:
            stack.close()
        except Exception as error:
            logger.exception("Gateway connection cleanup failed")
            raise GatewayUnavailableError(GATEWAY_UNAVAILABLE_MESSAGE) from error


# ── TODO 8 — Agent Entrypoint ─────────────────────────────────────────────────
# Implement the invoke() function decorated with @app.entrypoint.
#
# Steps:
#   1. Extract user_input, actor_id, and session_id from the payload
#      (generate a UUID if session_id is missing)
#   2. Instantiate MemoryHook for this actor/session
#   3. Instantiate AgentCoreBrowser(region=REGION)
#   4. Build the tools list: [search_knowledge_base, calculate_loyalty_discount,
#                              agent_core_browser.browser]
#   5. Connect to the Gateway via MCPClient, load gateway_tools, extend tools list
#   6. Create and invoke the Agent with all tools, hooks, and system_prompt
#   7. Return the text from the first content block of the response
#   8. Handle exceptions gracefully

@app.entrypoint
async def invoke(payload, context=None):
    """
    Main handler called by AgentCore for every incoming request.

    Expected payload keys:
      prompt      (str, required) — the customer's message
      customer_id (str, optional) — unique customer identifier
      session_id  (str, optional) — session identifier; generated if absent
    """
    # TODO: Implement the agent invocation
    try:
        user_input = payload.get("prompt", "")

        if not isinstance(user_input, str) or not user_input.strip():
            return "Please provide a non-empty prompt."

        actor_id = payload.get("customer_id") or str(uuid.uuid4())
        session_id = payload.get("session_id") or str(uuid.uuid4())

        memory_hook = MemoryHook(
            actor_id,
            session_id,
            memory_client,
            MEMORY_ID
        )

        agent_core_browser = AgentCoreBrowser(region=REGION)

        tools = [
            search_knowledge_base,
            calculate_loyalty_discount,
            agent_core_browser.browser,
        ]

        with gateway_tool_session() as gateway_tools:
            tools.extend(gateway_tools)

            system_prompt = (
                "You are a helpful customer support assistant "
                "for a fictional e-commerce store. "
                "Use order and refund tools for customer actions, "
                "the knowledge base for product and policy information, "
                "the discount calculator for loyalty arithmetic, "
                "and the browser for current web information. "
                "Never invent tool results. "
                "Refund tools are mock operations, not real transactions."
            )

            agent = Agent(
                model=model,
                tools=tools,
                hooks=[memory_hook],
                system_prompt=system_prompt,
            )

            response = await agent.invoke_async(user_input)

            return response.message["content"][0].get("text", "")

    except GatewayUnavailableError:
        return GATEWAY_UNAVAILABLE_MESSAGE

    except Exception:
        logger.exception("Agent invocation failed")

        return (
            "Sorry, the support agent encountered an error. "
            "Please try again."
        )


# ── CLI entry point (do not modify) ──────────────────────────────────────────
def main():
    """Run one invocation from the command line for local testing."""
    parser = argparse.ArgumentParser()
    parser.add_argument("payload", type=str)
    args = parser.parse_args()
    response = asyncio.run(invoke(json.loads(args.payload)))
    print(response)


if __name__ == "__main__":
    app.run()
    # Uncomment the line below and comment app.run() for local CLI testing:
    # main()
