---
name: claude-artifacts-conventions
description: >
  Naming convention and folder hierarchy rules for all files inside the .claude
  directory of the Claude-Artifacts repository. Load this skill whenever
  validating, creating, or reviewing skills, commands, or agents.
---

# Claude Artifacts — Folder Hierarchy & Naming Conventions

This is the authoritative reference for how files must be organised inside the
`.claude/` directory. These rules are enforced automatically by the pre-hook
that runs before every `/devops:raise-pr` execution.

---

## Folder Structure

All three folders follow the same three-level hierarchy:

```
.claude/
├── skills/
│   └── {team-name}/
│       └── {skill-name}/
│           └── SKILL.md          ← required entry-point file
│               [supporting files and subdirectories are allowed here]
│
├── commands/
│   └── {team-name}/
│       └── {command-name}/
│           └── {command-name}.md ← filename must match folder name
│               [supporting files and subdirectories are allowed here]
│
└── agents/
    └── {team-name}/
        └── {agent-name}/
            └── {agent-name}.md   ← filename must match folder name
                [supporting files and subdirectories are allowed here]
```

---

## Naming Rules

### Team name  (`{team-name}`)
| Rule | Example (valid) | Example (invalid) |
|------|----------------|-------------------|
| All lowercase | `engineering` | `Engineering` |
| Letters, numbers, hyphens only | `cloud-native-engineering` | `cloud_native_engineering` |
| No spaces | `pm` | `project management` |
| No uppercase | `cne` | `CNE` |

### Skill / Command / Agent folder name (`{skill-name}`, `{command-name}`, `{agent-name}`)
| Rule | Example (valid) | Example (invalid) |
|------|----------------|-------------------|
| All lowercase | `api-designer` | `Api-Designer` |
| Words separated by hyphens | `flowchart-generator` | `flowchart_generator` |
| No spaces | `pull-code` | `pull code` |
| No underscores | `jira-update` | `jira_update` |
| No uppercase | `eng-document-feature` | `engDocumentFeature` |

### Entry-point file names
| Folder | Required filename | Notes |
|--------|------------------|-------|
| `skills/` | `SKILL.md` | Always uppercase, always this exact name |
| `commands/` | `{command-name}.md` | Must match the containing folder name |
| `agents/` | `{agent-name}.md` | Must match the containing folder name |

---

## Supporting Files

Skills, commands, and agents may include additional supporting files
(references, scripts, assets, templates) inside subdirectories. These are
**not** subject to the entry-point naming rule but their parent folder must
still comply with the team/item-name structure.

```
.claude/skills/devops/iac-terraform/   ← valid team/skill structure
    SKILL.md                            ← required entry-point
    references/                         ← supporting subdirectory (allowed)
        best_practices.md
    scripts/                            ← supporting subdirectory (allowed)
        validate_module.py
    assets/
        workflows/
            github-actions-terraform.yml
```

---

## Teams currently registered

| Team folder | Description |
|-------------|-------------|
| `agile` | Agile / Scrum practices |
| `ba` | Business Analysis |
| `cne` | Cloud Native Engineering |
| `cne2` | Cloud Native Engineering 2 |
| `cloud-native-engineering` | Cloud Native Engineering (legacy) |
| `design` | UX / Design |
| `devops` | DevOps / Infrastructure |
| `engineering` | Software Engineering |
| `miscellaneous` | Items not yet assigned to a team |
| `org` | Org-wide reference skills |
| `pm` | Project / Product Management |
| `product-management` | Product Management (legacy) |
| `project-management` | Project Management (legacy) |
| `sales` | Sales |
| `set` | SET team |

To add a new team, create a new lowercase folder directly inside
`.claude/skills/`, `.claude/commands/`, or `.claude/agents/`.

---

## Quick-reference checklist before raising a PR

- [ ] Skill/command/agent is inside a **team folder** (lowercase)
- [ ] Team folder name uses **only lowercase letters, numbers, and hyphens**
- [ ] Skill/command/agent has its **own subfolder** (not placed directly in team folder)
- [ ] Subfolder name uses **only lowercase letters, numbers, and hyphens**
- [ ] Skills entry-point file is named **`SKILL.md`** (uppercase)
- [ ] Commands/agents entry-point file is named **`{folder-name}.md`** (matches folder)
- [ ] No spaces or underscores anywhere in folder names
