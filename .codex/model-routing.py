#!/usr/bin/env python3
"""Fixture-testable policy for Mimir's configured Codex PreToolUse hook.

Fixtures exercise the documented Codex event fields; they do not establish
live hook execution or enforcement.
"""
import json
import sys

ROLES = {
    "mimir_routine": "gpt-6-luna",
    "mimir_reviewer": "gpt-6.2-sol",
}
SPAWN_TOOLS = {"Agent", "spawn_agent"}
ROUTINE_TOOLS = {
    "Bash", "Shell", "exec_command", "apply_patch", "Edit", "Write",
    "write_stdin",
}


def valid_spawn(tool_input, caller_model):
    """Require a Sol caller, exact target profile/model pair, and fresh turns."""
    if not isinstance(tool_input, dict) or caller_model != "gpt-6.2-sol":
        return False
    role = tool_input.get("agent_type")
    model = tool_input.get("model")
    return (
        role in ROLES
        and model == ROLES[role]
        and tool_input.get("fork_turns") == "none"
    )


def deny(reason):
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }


def _allow():
    return {"hookSpecificOutput": {
        "hookEventName": "PreToolUse", "permissionDecision": "allow"
    }}


def handle(event):
    """Return an allow/deny result for a hook event or a test fixture."""
    if not isinstance(event, dict):
        return deny("Mimir routing hook expected a JSON object.")
    if event.get("hook_event_name") not in (None, "PreToolUse"):
        return deny("Mimir routing hook received an unexpected event.")

    tool_name = event.get("tool_name", "Agent")
    caller_model = event.get("model")

    if tool_name in SPAWN_TOOLS:
        tool_input = event.get("tool_input", event)
        if not valid_spawn(tool_input, caller_model):
            return deny(
                "Only a gpt-6.2-sol caller may launch mimir_routine/gpt-6-luna "
                "or mimir_reviewer/gpt-6.2-sol with fork_turns: none."
            )
        return _allow()

    if tool_name in ROUTINE_TOOLS:
        if caller_model != "gpt-6-luna":
            return deny(
                "Shell, edit, write, and command tools are allowed only when "
                "the current model is gpt-6-luna."
            )
        return _allow()

    return _allow()


def main():
    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, UnicodeDecodeError):
        result = deny("Mimir routing hook received invalid JSON.")
    else:
        result = handle(event)
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
