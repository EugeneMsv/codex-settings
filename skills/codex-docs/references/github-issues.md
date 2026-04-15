# openai/codex GitHub Issues

Use live GitHub issue checks to detect current bugs, regressions, docs gaps, and workarounds before changing Codex configuration.

## Preferred Lookup Order

1. GitHub MCP, if configured and available.
2. `gh` CLI, if installed and authenticated.
3. Browser or web search fallback to `https://github.com/openai/codex/issues`.

## gh Commands

List likely matches:

```bash
gh issue list --repo openai/codex --search "config.toml in:title,body" --limit 20
```

View details:

```bash
gh issue view --repo openai/codex ISSUE_NUMBER --comments
```

Search GitHub syntax examples:

```text
config.toml in:title,body
.codex/config.toml in:title,body
requirements.toml in:title,body
mcp_servers in:title,body
sandbox_mode in:title,body
approval_policy in:title,body
model_provider in:title,body
hooks in:title,body
rules in:title,body
skills in:title,body
subagents in:title,body
```

## Classification

- **Bug**: current Codex behavior contradicts official docs or expected config behavior.
- **Regression**: issue reports behavior changed from a prior version.
- **Docs gap**: current docs omit a key, edge case, or setup step.
- **Workaround**: a maintainer or multiple users describe a practical temporary fix.
- **Feature idea**: recurring request or pain point that could become a Codex improvement proposal.

## Reporting

When issue findings affect advice, include:

- Issue number and title
- Open or closed state
- Why it matters to the user's config
- Whether the recommendation comes from official docs, a maintainer comment, or user reports

Do not bake static issue summaries into the skill. Always check live issues for current status.
