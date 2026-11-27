import importlib.util
import re
import sys
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / ".codex/model-routing.py"
SPEC = importlib.util.spec_from_file_location("model_routing", MODULE_PATH)
model_routing = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(model_routing)
LIFECYCLE_PATH = ROOT / "scripts/mimir-lifecycle.py"
LIFECYCLE_SPEC = importlib.util.spec_from_file_location("mimir_lifecycle", LIFECYCLE_PATH)
lifecycle = importlib.util.module_from_spec(LIFECYCLE_SPEC)
sys.modules[LIFECYCLE_SPEC.name] = lifecycle
LIFECYCLE_SPEC.loader.exec_module(lifecycle)


def decision(event):
    return model_routing.handle(event)["hookSpecificOutput"]["permissionDecision"]


class ModelRoutingTests(unittest.TestCase):
    def test_policy_tool_sets_match_configured_pretooluse_matcher(self):
        config = (ROOT / ".codex/config.toml").read_text()
        matcher = re.search(r'(?m)^matcher = "([^"]+)"$', config)
        self.assertIsNotNone(matcher)
        alternatives = re.fullmatch(r"\^\(([^()]*)\)\$", matcher.group(1))
        self.assertIsNotNone(alternatives)
        configured_tools = set(alternatives.group(1).split("|"))
        self.assertEqual(
            configured_tools,
            model_routing.SPAWN_TOOLS | model_routing.ROUTINE_TOOLS,
        )

    def test_sol_can_launch_exact_fresh_routine_and_reviewer_profiles(self):
        for role, model in model_routing.ROLES.items():
            with self.subTest(role=role):
                self.assertEqual(decision({
                    "hook_event_name": "PreToolUse", "tool_name": "Agent",
                    "model": "gpt-6.2-sol",
                    "tool_input": {
                        "agent_type": role, "model": model,
                        "fork_turns": "none",
                    },
                }), "allow")

    def test_spawn_uses_only_documented_target_and_caller_fields(self):
        event = {
            "hook_event_name": "PreToolUse", "tool_name": "spawn_agent",
            "model": "gpt-6.2-sol",
            "tool_input": {
                "agent_type": "mimir_routine", "model": "gpt-6-luna",
                "fork_turns": "none",
            },
        }
        self.assertEqual(decision(event), "allow")
        # Undocumented role aliases cannot substitute for the target field.
        event["tool_input"] = {
            "role": "mimir_routine", "model": "gpt-6-luna",
            "fork_turns": "none",
        }
        self.assertEqual(decision(event), "deny")

    def test_rejects_wrong_caller_model_target_and_inherited_turns(self):
        base = {
            "hook_event_name": "PreToolUse", "tool_name": "Agent",
            "model": "gpt-6.2-sol",
            "tool_input": {
                "agent_type": "mimir_routine", "model": "gpt-6-luna",
                "fork_turns": "none",
            },
        }
        cases = [
            ({**base, "model": "gpt-6-luna"}, "non-Sol caller"),
            ({**base, "tool_input": {**base["tool_input"], "model": "gpt-6.2-sol"}}, "wrong role/model pair"),
            ({**base, "tool_input": {**base["tool_input"], "agent_type": "other"}}, "unknown role"),
            ({**base, "tool_input": {**base["tool_input"], "fork_turns": "all"}}, "inherited turns"),
        ]
        for event, label in cases:
            with self.subTest(case=label):
                self.assertEqual(decision(event), "deny")

    def test_only_luna_model_can_use_command_and_edit_tools(self):
        for tool in model_routing.ROUTINE_TOOLS:
            with self.subTest(tool=tool):
                self.assertEqual(decision({
                    "tool_name": tool,
                    "model": "gpt-6-luna",
                }), "allow")
                self.assertEqual(decision({
                    "tool_name": tool,
                    "model": "gpt-6.2-sol",
                }), "deny")
                self.assertEqual(decision({"tool_name": tool}), "deny")

    def test_target_config_omits_only_clone_approval_defaults(self):
        rendered = lifecycle.expected_content(ROOT, ".codex/config.toml", False).decode()
        self.assertIn('model = "gpt-6.2-sol"', rendered)
        self.assertIn('model_reasoning_effort = "high"', rendered)
        self.assertIn("[agents]", rendered)
        self.assertIn("enabled = true", rendered)
        self.assertIn("max_concurrent_threads_per_session = 4", rendered)
        self.assertIn("[[hooks.PreToolUse]]", rendered)
        self.assertIn(".codex/model-routing.py", rendered)
        for key in ("sandbox_mode", "approval_policy", "approvals_reviewer"):
            self.assertNotIn(key + " =", rendered)

    def test_reviewer_profile_declares_capability_limits_without_claiming_isolation(self):
        profile = (ROOT / ".codex/agents/mimir_reviewer.toml").read_text()
        self.assertIn('model = "gpt-6.2-sol"', profile)
        self.assertIn('model_reasoning_effort = "high"', profile)
        self.assertIn("tools = []", profile)
        for feature in ("shell_tool", "apps", "plugins", "memories", "request_permissions_tool"):
            self.assertIn(feature + " = false", profile)
        self.assertIn("Custom-agent sandbox inheritance and runtime", profile)
        self.assertIn("enforcement are unverified.", profile)


if __name__ == "__main__":
    unittest.main()
