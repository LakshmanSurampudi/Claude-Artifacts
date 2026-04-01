#!/usr/bin/env python3
"""
Pre-hook: Validates .claude/skills, .claude/commands, and .claude/agents
naming conventions before /devops:raise-pr is allowed to run.

Exit codes:
  0 → allow the tool call to proceed
  2 → block the tool call and show the violation report to the user
"""

import json
import re
import subprocess
import sys


# Matches valid team/folder names: lowercase letters, digits, hyphens only
VALID_NAME = re.compile(r'^[a-z0-9][a-z0-9-]*$')


# ── Helpers ──────────────────────────────────────────────────────────────────

def get_new_files():
    """Return files present on origin/main (the fork) but absent on upstream/main
    (the PR target). These are exactly the new files the PR would introduce.
    """
    try:
        # Ensure both remote refs are up-to-date before diffing
        subprocess.run(["git", "fetch", "origin", "main", "--quiet"], capture_output=True)
        subprocess.run(["git", "fetch", "upstream", "main", "--quiet"], capture_output=True)
        result = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=A", "upstream/main", "origin/main"],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            return []
        return [f.strip() for f in result.stdout.strip().splitlines() if f.strip()]
    except Exception:
        return []


def err(filepath, *messages):
    """Format a single violation entry."""
    lines = [f"  {filepath}"]
    for msg in messages:
        lines.append(f"    → {msg}")
    return "\n".join(lines)


# ── Validators ────────────────────────────────────────────────────────────────

def validate_skills(parts, filepath):
    """
    Rule: .claude/skills/{team}/{skill-name}/SKILL.md
    Files deeper than 3 parts are supporting files — skip them.
    Files shallower than 3 parts are always violations.
    """
    if len(parts) > 3:
        return None  # supporting file inside skill folder — allowed
    if len(parts) < 3:
        return err(filepath, "too shallow — expected team/skill-name/SKILL.md")

    team, skill_name, filename = parts
    problems = []

    if not VALID_NAME.match(team):
        problems.append(
            f"team name '{team}' must be lowercase letters/numbers/hyphens only "
            f"(no uppercase, spaces, or underscores)"
        )
    if not VALID_NAME.match(skill_name):
        problems.append(
            f"skill folder '{skill_name}' must be lowercase letters/numbers/hyphens only "
            f"(no uppercase, spaces, or underscores)"
        )
    if filename != "SKILL.md":
        problems.append(
            f"entry-point file must be named 'SKILL.md' (got '{filename}')"
        )

    return err(filepath, *problems) if problems else None


def validate_commands(parts, filepath):
    """
    Rule: .claude/commands/{team}/{command-name}/{command-name}.md
    Files deeper than 3 parts are supporting files — skip them.
    """
    if len(parts) > 3:
        return None
    if len(parts) < 3:
        return err(filepath, "too shallow — expected team/command-name/command-name.md")

    team, cmd_name, filename = parts
    expected_file = f"{cmd_name}.md"
    problems = []

    if not VALID_NAME.match(team):
        problems.append(
            f"team name '{team}' must be lowercase letters/numbers/hyphens only"
        )
    if not VALID_NAME.match(cmd_name):
        problems.append(
            f"command folder '{cmd_name}' must be lowercase letters/numbers/hyphens only"
        )
    if filename != expected_file:
        problems.append(
            f"entry-point file must be named '{expected_file}' to match folder name "
            f"(got '{filename}')"
        )

    return err(filepath, *problems) if problems else None


def validate_agents(parts, filepath):
    """
    Rule: .claude/agents/{team}/{agent-name}/{agent-name}.md
    Files deeper than 3 parts are supporting files — skip them.
    """
    if len(parts) > 3:
        return None
    if len(parts) < 3:
        return err(filepath, "too shallow — expected team/agent-name/agent-name.md")

    team, agent_name, filename = parts
    expected_file = f"{agent_name}.md"
    problems = []

    if not VALID_NAME.match(team):
        problems.append(
            f"team name '{team}' must be lowercase letters/numbers/hyphens only"
        )
    if not VALID_NAME.match(agent_name):
        problems.append(
            f"agent folder '{agent_name}' must be lowercase letters/numbers/hyphens only"
        )
    if filename != expected_file:
        problems.append(
            f"entry-point file must be named '{expected_file}' to match folder name "
            f"(got '{filename}')"
        )

    return err(filepath, *problems) if problems else None


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    # Ensure UTF-8 output on Windows (avoids cp1252 UnicodeEncodeError for emoji)
    sys.stdout.reconfigure(encoding="utf-8")

    # 1. Parse the tool-call JSON from stdin
    try:
        tool_call = json.loads(sys.stdin.read())
    except Exception:
        sys.exit(0)  # can't parse → don't block

    tool_name = tool_call.get("tool_name", "")
    tool_input = tool_call.get("tool_input", {})

    # 2. Only intercept Skill calls that include "raise-pr"
    if tool_name != "Skill":
        sys.exit(0)

    skill = tool_input.get("skill", "").lower()
    if "raise-pr" not in skill:
        sys.exit(0)

    # 3. Collect new files added in this branch
    new_files = get_new_files()
    if not new_files:
        sys.exit(0)

    # 4. Validate each new file that lives inside .claude/skills|commands|agents
    violations = []

    for filepath in new_files:
        if filepath.startswith(".claude/skills/"):
            parts = filepath[len(".claude/skills/"):].split("/")
            result = validate_skills(parts, filepath)
        elif filepath.startswith(".claude/commands/"):
            parts = filepath[len(".claude/commands/"):].split("/")
            result = validate_commands(parts, filepath)
        elif filepath.startswith(".claude/agents/"):
            parts = filepath[len(".claude/agents/"):].split("/")
            result = validate_agents(parts, filepath)
        else:
            result = None

        if result:
            violations.append(result)

    # 5. Report and exit
    if not violations:
        sys.exit(0)

    print("❌  PR blocked — naming convention violations detected in .claude/\n")
    print(f"Found {len(violations)} violation(s):\n")
    for v in violations:
        print(v)
        print()

    print("── Expected structure ──────────────────────────────────────────")
    print("  skills/   →  .claude/skills/{team}/{skill-name}/SKILL.md")
    print("  commands/ →  .claude/commands/{team}/{command-name}/{command-name}.md")
    print("  agents/   →  .claude/agents/{team}/{agent-name}/{agent-name}.md")
    print()
    print("── Naming rules ────────────────────────────────────────────────")
    print("  • team & folder names : lowercase, hyphens allowed")
    print("                          e.g.  engineering   cloud-native-engineering")
    print("  • NO uppercase, spaces, or underscores in folder names")
    print("  • skills file         : must be SKILL.md  (uppercase)")
    print("  • command/agent file  : must match folder name  e.g. pull-code.md")
    print()
    print("Fix the violations above, then run /devops:raise-pr again.")
    print()
    print("Reference: .claude/skills/org/claude-artifacts-conventions/SKILL.md")

    sys.exit(2)


if __name__ == "__main__":
    main()
