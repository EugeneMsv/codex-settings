---
name: codex-docs
description: Use when configuring or troubleshooting Codex, including config.toml, project .codex/config.toml, requirements.toml, MCP servers, rules, hooks, skills, subagents, sandbox and approval settings, model providers, GitHub integration, or when checking openai/codex GitHub issues for current bugs, docs gaps, workarounds, or feature ideas.
---

# Codex Docs

Use this skill to configure Codex with current official documentation and live `openai/codex` issue context.

## Core Workflow

1. Identify the user's mode:
   - **Advisor**: inspect context and propose exact safe changes.
   - **Fixer**: edit requested Codex config, rules, hooks, MCP, skills, or subagent files.
   - **Feature scout**: use docs and issues to propose Codex improvements or docs updates.
2. Inspect local non-secret context first:
   - User config: `~/.codex/config.toml`
   - Project config: `.codex/config.toml`
   - Project requirements: `.codex/requirements.toml`
   - Rules: `AGENTS.md`, `.codex/rules/`, and configured rule locations
   - Skill and subagent metadata when relevant
3. Fetch current official Codex docs before advising on config keys or behavior. Use `references/codex-doc-map.md` to choose pages.
4. Check live `openai/codex` GitHub issues for current bugs, regressions, docs gaps, and workarounds. Use `references/github-issues.md`.
5. Compare docs, local config, and issue findings. Treat official docs as the source of truth unless a GitHub issue clearly documents a current bug or regression.
6. Present a concise diagnosis with:
   - Relevant local findings
   - Official docs source
   - GitHub issue signal, if any
   - Exact proposed changes
   - Verification command
7. Edit only when the user asks for implementation. Keep edits scoped and avoid unrelated formatting churn.
8. Verify after edits with the narrowest useful check, such as TOML parsing, `codex --help`, `codex mcp list`, or the local helper script.

## Safety Rules

- Do not read, print, summarize, or copy `auth.json`, `.env`, private keys, OAuth tokens, API keys, credential stores, or secret directories unless the user explicitly requests it and permission allows it.
- Do not modify authentication state, delete config, or run destructive Git or shell commands unless the user explicitly asks and approves.
- When editing config, preserve unrelated user settings and comments where practical.
- Prefer current official OpenAI Codex docs over memory for fast-moving keys, defaults, or behavior.
- If docs and GitHub issues conflict, state the conflict and recommend the least risky path.

## Configuration Guidance

- For user-wide settings, prefer `~/.codex/config.toml`.
- For project-specific settings, use `.codex/config.toml` only when the project is trusted and the setting belongs to that project.
- For reusable instructions, prefer `AGENTS.md` or `.codex/rules/` according to current docs and local project conventions.
- For repeatable specialized workflows, prefer a skill with `SKILL.md` and optional `references/`, `scripts/`, or `assets/`.
- For external tools, configure MCP servers only after checking current docs and any known `openai/codex` issues for that server type.

## Verification

Use the bundled script for local config sanity checks:

```bash
python3 ~/.codex/skills/codex-docs/scripts/check_codex_config.py
```

For explicit files:

```bash
python3 ~/.codex/skills/codex-docs/scripts/check_codex_config.py ~/.codex/config.toml .codex/config.toml
```

The script validates TOML syntax and reports common missing local path references without reading secret files.
