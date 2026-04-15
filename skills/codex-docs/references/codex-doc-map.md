# Codex Documentation Map

Fetch current official docs before advising on fast-moving Codex behavior. Do not paste large copied docs into this skill.

## Primary Pages

- Config reference: `https://developers.openai.com/codex/config-reference`
  - Use for exact `config.toml` keys, value types, defaults, and schema guidance.
- Advanced config: `https://developers.openai.com/codex/config-advanced`
  - Use for config precedence, profiles, CLI overrides, project `.codex/config.toml`, model providers, sandbox, and approval behavior.
- Sample config: `https://developers.openai.com/codex/config-sample`
  - Use for practical examples and TOML shapes.
- MCP: `https://developers.openai.com/codex/mcp`
  - Use for MCP server setup, transports, environment handling, and tool exposure.
- Rules: `https://developers.openai.com/codex/rules`
  - Use for project or user instructions, rule file locations, and precedence.
- Hooks: `https://developers.openai.com/codex/hooks`
  - Use for lifecycle automation and command safety.
- Skills: `https://developers.openai.com/codex/skills`
  - Use for skill structure, locations, metadata, and progressive disclosure.
- Subagents: `https://developers.openai.com/codex/subagents`
  - Use for agent roles and delegation configuration.
- GitHub integration: `https://developers.openai.com/codex/integrations/github`
  - Use for GitHub app, PR review, repository integration, and cloud workflows.

## Lookup Pattern

1. Choose the smallest relevant page from the map.
2. Fetch current docs and cite the page used.
3. Cross-check `openai/codex` GitHub issues for current bugs or workarounds.
4. Distinguish documented behavior from inferred behavior.
5. If docs are missing or ambiguous, say so and treat any recommendation as a conservative default.

## Common Task Routing

- `config.toml`, profiles, model providers, sandbox, approval policy: config reference and advanced config.
- `.codex/config.toml` or `requirements.toml`: advanced config and config reference.
- GitHub MCP setup: MCP docs, GitHub integration docs, then GitHub issue search.
- Custom project instructions: rules docs and skills docs.
- Skill creation or installation: skills docs and local skill-creator guidance.
- Hooks and automation: hooks docs and config reference.
- Unexpected Codex behavior: relevant docs page, then live issue search.
