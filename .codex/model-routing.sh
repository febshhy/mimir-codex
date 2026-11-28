#!/usr/bin/env bash
# Bash/jq implementation of the configured Mimir Codex PreToolUse policy.
# Fixtures exercise documented event fields; they do not prove live enforcement.
set -u

deny() {
  jq -cn --arg reason "$1" '{hookSpecificOutput:{hookEventName:"PreToolUse",permissionDecision:"deny",permissionDecisionReason:$reason}}'
}

if result=$(jq -c '
  def deny($reason): {hookSpecificOutput:{hookEventName:"PreToolUse",permissionDecision:"deny",permissionDecisionReason:$reason}};
  def allow: {hookSpecificOutput:{hookEventName:"PreToolUse",permissionDecision:"allow"}};
  if type != "object" then
    deny("Mimir routing hook expected a JSON object.")
  elif (has("hook_event_name") and .hook_event_name != null and .hook_event_name != "PreToolUse") then
    deny("Mimir routing hook received an unexpected event.")
  else
    (if has("tool_name") then .tool_name else "Agent" end) as $tool |
    .model as $caller |
    (if has("tool_input") then .tool_input else . end) as $input |
    if (["Agent", "spawn_agent"] | index($tool)) != null then
      if ($input | type) == "object" and $caller == "gpt-6.2-sol" and
         ($input.agent_type as $role |
           (($role == "mimir_routine" and $input.model == "gpt-6-luna") or
            ($role == "mimir_reviewer" and $input.model == "gpt-6.2-sol")) and
           $input.fork_turns == "none") then
        allow
      else
        deny("Only a gpt-6.2-sol caller may launch mimir_routine/gpt-6-luna or mimir_reviewer/gpt-6.2-sol with fork_turns: none.")
      end
    elif (["Bash", "Shell", "exec_command", "apply_patch", "Edit", "Write", "write_stdin"] | index($tool)) != null then
      if $caller == "gpt-6-luna" then allow
      else deny("Shell, edit, write, and command tools are allowed only when the current model is gpt-6-luna.") end
    else
      allow
    end
  end
' 2>/dev/null); then
  printf '%s\n' "$result"
else
  deny 'Mimir routing hook received invalid JSON.'
fi
