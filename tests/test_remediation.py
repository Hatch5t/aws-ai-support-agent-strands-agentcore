"""Offline Attempt 2 regressions. No AWS SDK or live endpoint is used."""
import asyncio
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import socket
import sys
import types
import unittest
from unittest.mock import AsyncMock, MagicMock, Mock, patch, sentinel


REQUIRED = {
    "points_redeemed", "points_discount", "tier_discount_pct", "tier_discount",
    "final_total", "total_savings", "points_earned", "remaining_points",
}


def load_agent():
    """Import the actual application with external libraries replaced by stubs."""
    modules = {}
    names = [
        "strands", "strands.models", "strands.hooks", "strands.tools",
        "strands.tools.mcp", "strands.tools.mcp.mcp_client", "strands_tools",
        "strands_tools.browser", "bedrock_agentcore", "bedrock_agentcore.runtime",
        "bedrock_agentcore.memory", "bedrock_agentcore.tools",
        "bedrock_agentcore.tools.code_interpreter_client", "mcp", "mcp.client",
        "mcp.client.streamable_http", "boto3",
    ]
    for name in names:
        modules[name] = types.ModuleType(name)
        modules[name].__path__ = []
    modules["strands"].tool = lambda function: function
    modules["strands"].Agent = Mock()
    modules["strands.models"].BedrockModel = Mock()
    for name in ["HookProvider", "HookRegistry", "AfterInvocationEvent", "MessageAddedEvent"]:
        setattr(modules["strands.hooks"], name, type(name, (), {}))

    class App:
        def entrypoint(self, function):
            return function
        def run(self):
            raise AssertionError("The Runtime server must not start in offline tests")

    modules["bedrock_agentcore.runtime"].BedrockAgentCoreApp = App
    modules["bedrock_agentcore.memory"].MemoryClient = Mock()
    modules["bedrock_agentcore.memory"].MemoryClient.return_value.get_memory_strategies.return_value = []
    modules["bedrock_agentcore.tools.code_interpreter_client"].code_session = Mock()
    modules["strands.tools.mcp.mcp_client"].MCPClient = Mock()
    modules["mcp.client.streamable_http"].streamable_http_client = Mock()
    modules["strands_tools.browser"].AgentCoreBrowser = Mock()
    modules["boto3"].client = Mock()
    source = Path(__file__).resolve().parents[1] / "starter" / "main.py"
    spec = importlib.util.spec_from_file_location("attempt2_agent_under_test", source)
    module = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, modules), patch.dict(os.environ), patch.object(
        socket, "socket", side_effect=AssertionError("Network forbidden in offline tests")
    ):
        spec.loader.exec_module(module)
    return module


class OfflineCase(unittest.TestCase):
    def setUp(self):
        self.agent = load_agent()
        self.network = patch.object(
            socket, "create_connection", side_effect=AssertionError("Network forbidden in offline tests")
        )
        self.network.start()
        self.addCleanup(self.network.stop)


class GatewayTests(OfflineCase):
    def setUp(self):
        super().setUp()
        self.gateway = MagicMock()
        self.gateway.__enter__.return_value = self.gateway
        self.gateway.list_tools_sync.return_value = [sentinel.order, sentinel.refund]
        self.agent.MCPClient.return_value = self.gateway
        response = types.SimpleNamespace(message={"content": [{"text": "successful answer"}]})
        self.runner = types.SimpleNamespace(invoke_async=AsyncMock(return_value=response))
        self.agent.Agent.return_value = self.runner

    def invoke(self):
        return asyncio.run(self.agent.invoke({
            "prompt": "Track the demonstration order", "customer_id": "CUST-123",
            "session_id": "offline-test",
        }))

    def unavailable(self, expected_log):
        with self.assertLogs("CSAI_Agent", level="INFO") as logs:
            result = self.invoke()
        self.assertEqual(result, self.agent.GATEWAY_UNAVAILABLE_MESSAGE)
        self.assertNotIn("internal detail", result)
        self.assertNotIn(self.agent.GATEWAY_URL, result)
        self.assertTrue(any(expected_log in line for line in logs.output), logs.output)
        self.agent.Agent.assert_not_called()

    def test_success_preserves_tools_transport_and_response(self):
        with self.assertLogs("CSAI_Agent", level="INFO") as logs:
            self.assertEqual(self.invoke(), "successful answer")
        self.assertTrue(any("Discovered 2 Gateway tools" in line for line in logs.output))
        tools = self.agent.Agent.call_args.kwargs["tools"]
        self.assertIn(sentinel.order, tools)
        self.assertIn(sentinel.refund, tools)
        self.assertIn(self.agent.search_knowledge_base, tools)
        self.assertIn(self.agent.calculate_loyalty_discount, tools)
        self.assertIn(self.agent.AgentCoreBrowser.return_value.browser, tools)
        self.agent.MCPClient.call_args.args[0]()
        self.agent.streamable_http_client.assert_called_once_with(self.agent.GATEWAY_URL)
        self.gateway.__exit__.assert_called_once()
        self.agent.AgentCoreBrowser.assert_called_once_with(region=self.agent.REGION)

    def test_timeout_entering_context(self):
        self.gateway.__enter__.side_effect = TimeoutError("internal detail")
        self.unavailable("timed out")
        self.gateway.list_tools_sync.assert_not_called()

    def test_timeout_discovering_tools(self):
        self.gateway.list_tools_sync.side_effect = TimeoutError("internal detail")
        self.unavailable("timed out")
        self.gateway.__exit__.assert_called_once()

    def test_connection_failure_entering_context(self):
        self.gateway.__enter__.side_effect = ConnectionError("internal detail")
        self.unavailable("connection or tool discovery failed")

    def test_connection_failure_discovering_tools(self):
        self.gateway.list_tools_sync.side_effect = ConnectionError("internal detail")
        self.unavailable("connection or tool discovery failed")

    def test_unexpected_discovery_failure(self):
        self.gateway.list_tools_sync.side_effect = RuntimeError("internal detail")
        self.unavailable("Unexpected Gateway")

    def test_unexpected_context_entry_failure(self):
        self.gateway.__enter__.side_effect = RuntimeError("internal detail")
        self.unavailable("Unexpected Gateway")

    def test_client_construction_failure(self):
        self.agent.MCPClient.side_effect = TimeoutError("internal detail")
        self.unavailable("timed out")

    def test_empty_discovery_is_not_success(self):
        self.gateway.list_tools_sync.return_value = []
        self.unavailable("returned no tools")

    def test_cleanup_failure_returns_safe_gateway_error(self):
        self.gateway.__exit__.side_effect = ConnectionError("internal detail")
        with self.assertLogs("CSAI_Agent", level="INFO"):
            self.assertEqual(self.invoke(), self.agent.GATEWAY_UNAVAILABLE_MESSAGE)

    def test_agent_failure_is_not_misreported_as_gateway_failure(self):
        self.runner.invoke_async.side_effect = TimeoutError("internal model detail")
        with self.assertLogs("CSAI_Agent", level="INFO"):
            result = self.invoke()
        self.assertIn("support agent encountered an error", result)
        self.assertNotEqual(result, self.agent.GATEWAY_UNAVAILABLE_MESSAGE)
        self.gateway.__exit__.assert_called_once()


class LoyaltyTests(OfflineCase):
    def setUp(self):
        super().setUp()
        self.client = MagicMock()
        self.session = MagicMock()
        self.session.__enter__.return_value = self.client
        self.agent.code_session.return_value = self.session
        self.client.invoke.side_effect = self.mock_execute

    def mock_execute(self, name, arguments):
        self.assertEqual(name, "executeCode")
        self.assertEqual(arguments["language"], "python")
        self.assertIs(arguments["clearContext"], True)
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            exec(compile(arguments["code"], "<mocked-sandbox-python>", "exec"), {})
        text = output.getvalue()
        return {"stream": iter([{"result": {
            "content": [{"type": "text", "text": text}],
            "structuredContent": {"stdout": text, "exitCode": 0}, "isError": False,
        }}])}

    def calculate(self, points=4250, tier="Gold", total=150, category="standard"):
        result = json.loads(self.agent.calculate_loyalty_discount(points, tier, total, category))
        self.assertTrue(REQUIRED <= result.keys())
        return result

    def test_exact_gold_regression_all_values(self):
        result = self.calculate()
        self.assertEqual(result, {
            "points_redeemed": 4000, "points_discount": 40.0,
            "tier_discount_pct": 0.10, "tier_discount": 11.0,
            "final_total": 99.0, "total_savings": 51.0,
            "points_earned": 99, "remaining_points": 349,
        })
        self.assertEqual(150 - result["points_discount"], 110.0)
        self.agent.code_session.assert_called_once_with(self.agent.REGION)

    def test_silver(self):
        result = self.calculate(tier="Silver")
        self.assertEqual((result["tier_discount_pct"], result["tier_discount"], result["final_total"], result["remaining_points"]), (0.0, 0.0, 110.0, 360))

    def test_platinum(self):
        result = self.calculate(tier="Platinum")
        self.assertEqual((result["tier_discount_pct"], result["tier_discount"], result["final_total"], result["remaining_points"]), (0.15, 16.5, 93.5, 343))

    def test_unknown_tier_has_zero_tier_discount(self):
        result = self.calculate(tier="Unknown")
        self.assertEqual((result["tier_discount_pct"], result["tier_discount"], result["final_total"]), (0.0, 0.0, 110.0))

    def test_zero_points(self):
        result = self.calculate(points=0)
        self.assertEqual((result["points_redeemed"], result["final_total"], result["remaining_points"]), (0, 135.0, 135))

    def test_insufficient_points(self):
        result = self.calculate(points=499)
        self.assertEqual((result["points_redeemed"], result["final_total"], result["remaining_points"]), (0, 135.0, 634))

    def test_redemption_cap(self):
        result = self.calculate(points=20000, tier="Platinum", total=100)
        self.assertEqual((result["points_redeemed"], result["points_discount"], result["final_total"], result["remaining_points"]), (5000, 50.0, 42.5, 15042))

    def test_redemption_rounds_down_to_500(self):
        self.assertEqual(self.calculate(points=4749)["points_redeemed"], 4500)

    def test_small_order_does_not_exceed_cap(self):
        result = self.calculate(points=5000, total=5)
        self.assertEqual((result["points_redeemed"], result["points_discount"], result["final_total"]), (0, 0.0, 4.5))

    def test_device_earning_rate(self):
        result = self.calculate(category="device")
        self.assertEqual((result["points_earned"], result["remaining_points"]), (198, 448))

    def test_fresh_earning_rate(self):
        result = self.calculate(category="fresh")
        self.assertEqual((result["points_earned"], result["remaining_points"]), (495, 745))

    def test_unknown_category_uses_standard_rate(self):
        self.assertEqual(self.calculate(category="unknown")["points_earned"], 99)

    def test_text_content_only_result_is_parsed(self):
        normal = self.mock_execute
        def text_only(name, arguments):
            result = normal(name, arguments)
            event = next(result["stream"])
            del event["result"]["structuredContent"]
            return {"stream": iter([event])}
        self.client.invoke.side_effect = text_only
        self.assertEqual(self.calculate()["tier_discount_pct"], 0.1)

    def test_structured_stdout_only_result_is_parsed(self):
        normal = self.mock_execute
        def stdout_only(name, arguments):
            event = next(normal(name, arguments)["stream"])
            event["result"]["content"] = []
            return {"stream": iter([event])}
        self.client.invoke.side_effect = stdout_only
        self.assertEqual(self.calculate()["final_total"], 99)

    def fallback(self):
        with self.assertLogs("CSAI_Agent", level="ERROR"):
            result = self.calculate()
        self.assertEqual(result, {
            "points_redeemed": 0, "points_discount": 0.0,
            "tier_discount_pct": 0.10, "tier_discount": 15.0,
            "final_total": 135.0, "total_savings": 15.0,
            "points_earned": 0, "remaining_points": 4250,
            "fallback": True,
            "message": "Code Interpreter unavailable. Tier discount only; points were not redeemed or earned.",
        })
        self.assertNotIn("internal detail", json.dumps(result))

    def test_code_interpreter_unavailable_has_consistent_fallback(self):
        self.agent.code_session.side_effect = ConnectionError("internal detail")
        self.fallback()

    def test_session_entry_failure_has_consistent_fallback(self):
        self.session.__enter__.side_effect = TimeoutError("internal detail")
        self.fallback()

    def test_invoke_failure_has_consistent_fallback(self):
        self.client.invoke.side_effect = RuntimeError("internal detail")
        self.fallback()

    def test_error_result_is_not_success(self):
        self.client.invoke.side_effect = None
        self.client.invoke.return_value = {"stream": iter([{"result": {"isError": True}}])}
        self.fallback()

    def test_nonzero_exit_code_is_not_success(self):
        self.client.invoke.side_effect = None
        self.client.invoke.return_value = {"stream": iter([{"result": {"content": [], "structuredContent": {"exitCode": 1}}}])}
        self.fallback()

    def test_missing_required_field_is_not_success(self):
        self.client.invoke.side_effect = None
        self.client.invoke.return_value = {"stream": iter([{"result": {"content": [{"type": "text", "text": '{"final_total":99}'}]}}])}
        self.fallback()

    def test_no_result_event_is_not_success(self):
        self.client.invoke.side_effect = None
        self.client.invoke.return_value = {"stream": iter([])}
        self.fallback()


class PassingFeatureRegressions(OfflineCase):
    def test_rag_still_calls_retrieve_and_joins_passages(self):
        self.agent._bedrock_runtime.retrieve.return_value = {
            "retrievalResults": [
                {"content": {"text": "Electronics: 15 days"}},
                {"content": {"text": "Original condition required"}},
            ]
        }
        self.assertEqual(
            self.agent.search_knowledge_base("electronics returns"),
            "Electronics: 15 days\n---\nOriginal condition required",
        )
        self.agent._bedrock_runtime.retrieve.assert_called_once_with(
            knowledgeBaseId=self.agent.KB_ID,
            retrievalQuery={"text": "electronics returns"},
        )

    def test_rag_missing_id_guard_is_preserved(self):
        self.agent.KB_ID = ""
        self.assertEqual(self.agent.search_knowledge_base("returns"), "Knowledge base not configured.")
        self.agent._bedrock_runtime.retrieve.assert_not_called()

    def test_rag_no_results_message_is_preserved(self):
        self.agent._bedrock_runtime.retrieve.return_value = {"retrievalResults": []}
        self.assertEqual(self.agent.search_knowledge_base("returns"), "No relevant knowledge base results found.")


if __name__ == "__main__":
    unittest.main()
