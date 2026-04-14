# Global Codex Instructions

## Global Instructions

Always:

- Be direct, concise, and factual. Avoid filler, praise, apology loops, and trailing "let me know" phrasing.
- Keep it simple. Do not over-plan or over-engineer straightforward work.
- Read the existing code and follow local patterns before changing anything.
- Keep edits scoped to the request. Do not rewrite unrelated code or metadata.
- Make changes as atomic as practical; group related edits to the same file together.
- Consider configured MCP servers or official documentation when the task involves unfamiliar or fast-moving APIs, tools, or dependencies.
- When producing temporary artifacts, create or reuse a relative `.codex` folder in the current git repository root, or in the working directory when not inside a git repo. Do not commit those temporary artifacts.
- Prefer practical implementation over speculative abstraction.
- Ask only when a missing choice materially changes the result and cannot be discovered locally.
- Treat credential files, `.env` files, private keys, OAuth tokens, and secret directories as off limits unless explicitly requested and allowed.

## Iterative Execution Protocol

For substantial implementation work:

1. Analyze the request using `mcp__sequentialthinking__sequentialthinking` when available.
2. Inspect the existing code.
3. Create a concise ordered TODO list when the work has multiple meaningful steps.
4. Task subjects must be numbered: `Task 1: ...`, `Task 2: ...`.
5. Every meaningful task must include verification, usually a focused test or the narrowest useful check.
6. Keep exactly one task in progress at a time.
7. Update or add tests during the task when the behavior is testable.
8. Test changes belong in the same task/commit as the code change.
9. A task is not complete until verification passes or the limitation is reported.
10. Do not start the next task until the previous task is complete.
11. Apply learnings from each task before starting the next.
12. When making testable claims such as "tests pass" or "code compiles", state the verification command and result.

Use Codex-native tools for progress tracking. If a checklist is useful, use `update_plan`, keep exactly one item `in_progress`, and track all changes.

## Communication Protocol

- Lead with the action taken or the answer.
- Use short sentences and active voice.
- Use bullets, numbered lists, tables, and code blocks only when they improve scanability.
- For multiple options, number them.
- For three or more approaches, use a compact comparison table when useful.
- Mention material risks or side effects before taking risky action.
- Do not display code unless it helps answer the question or the user asks.
- Keep final summaries focused on what changed, how it was verified, and what remains.
- Emoji markers are allowed in structured reviews, plans, and pros/cons when they improve scanability: warning/risk, error/blocker/missing, success/verified, con/removed, pro/added, changed, unchanged.

## Tool Usage

Required baseline for every implementation task:

- Read the relevant files before editing.
- Run verification commands or tests after changing behavior.
- Use `mcp__sequentialthinking__sequentialthinking` for complex planning or multi-step reasoning when available.
- Use `mcp__context7__resolve_library_id` and `mcp__context7__get_library_docs` before generating or changing code that depends on unfamiliar or fast-moving external libraries.
- Never use placeholders or guess missing parameters.

### Search And Reads

- Use `rg` for text search and `rg --files` for file discovery when available.
- Use bounded reads such as `sed -n` for large or uncertain files.
- Run independent reads/searches in parallel with `multi_tool_use.parallel` when practical.
- Prefer simple commands over pipelines when one command gives the needed signal.
- Treat generated files, large JSON files, OpenAPI specs, history files, logs, and `.codex` JSON files as large until 
  proven otherwise.
- For code navigation, symbol lookup, and codebase understanding, use this order when tools are available:
  1. LSP or semantic tools for definitions, references, symbols, hover docs, and diagnostics.
  2. Grep/text search for string literals and text-pattern searches.
  3. Glob/file discovery for file-name or path-pattern searches.
  4. Bash as the last resort for code search.
- Scope searches to the project or relevant config directory. Do not broad-search `/Users` or `~`.

### Edits

- Use `apply_patch` for manual file edits.
- Re-read a file before retrying an edit if it changed unexpectedly.
- Do not write source files with heredocs, `cat > file`, or shell redirection.
- Add imports in the same edit as the code that needs them.
- Keep unrelated formatting churn out of scoped changes.

### Documentation And Research

- Use official documentation for unfamiliar tools, configuration formats, APIs, and fast-moving libraries.
- If the user provides a documentation URL, read it before proceeding.
- Do not guess raw GitLab URLs; confirm file paths locally or with `glab`.
- If a web fetch returns 403 or 404, search for the correct official URL instead of retrying the same guessed URL.
- Prefer official sources over assumptions.

### Bash

- Use `python3`, not `python`, on macOS.
- Use `git --no-pager <subcommand>` when output may page.
- Do not use destructive commands unless the user explicitly asks and approval allows it.
- Avoid `sudo`, broad chmod/chown, force-push, `rm -rf`, cloud delete operations, `terraform destroy`, `helm uninstall/delete`, `flyway clean`, and package publishing unless explicitly requested and approved.

## Git Workflow

- Do not run destructive git commands unless explicitly requested.
- Do not revert user changes.
- Run `git add`, `git commit`, and `git push` as separate commands; verify each result before the next.
- Before creating a branch, run `git branch --list <branch>`; if it exists, ask how to proceed.
- Before adding a worktree, run `git worktree list`.
- Do not create worktrees inside `.claude` or `.codex`; use a sibling directory such as `../{repo}-{purpose}-{ref}`.
- Stash unstaged changes before `git pull --rebase` or branch checkout when needed, then pop after.
- On non-fast-forward push rejection, run `git pull --rebase` once, then push once. Do not retry a bare push.
- When `git pull` or `git pull --rebase` fails with "no tracking information", use `git pull --rebase origin $(git branch --show-current)` explicitly.
- Push with `git push origin $(git branch --show-current)` to avoid macOS branch-name casing issues.
- Do not amend pushed commits unless the user explicitly asks.
- When repository edits are requested and no branch context is provided, start from main, pull latest, then create a feature branch before file edits.
- Always create a feature branch before making file edits on main or master.
- Run project formatting/linting before each `git add` command when the project provides such checks.
- Run all relevant tests, including the full suite when the project workflow requires it, before `git add`; never commit known-failing tests unless the user explicitly asks.
- Use one commit per planned task when commits are requested.
- Commit only files relevant to the current task.
- For planned task commits, use `Task N: <description>` and do not combine unrelated tasks.
- To revert a committed file on a pushed branch, use `git checkout HEAD~1 -- <file>`, then create a new commit.

### GitLab

- Use `glab`, not `gh`, for GitLab repositories.
- Use `--opened`, `--closed`, `--merged`, or `--all` for `glab mr list`; do not use `--state`.
- Include `--fill` with non-interactive `glab mr create`.
- Do not use `glab ci view` non-interactively; use `glab ci status` or `glab ci get <id>`.
- Use single quotes for `glab api` URL arguments when special characters may appear.
- In `python3 -c` inline scripts, do not use `\!`; Python 3.12+ rejects it as an invalid escape. Use `!` unescaped in f-strings or write a temp script for complex cases.
- Assign MR: `glab mr update <id> --assignee <username>`.
- Update MR title: `glab mr update <id> --title "..."`.
- Get current GitLab username with `glab api user | python3 -c "import sys,json; print(json.load(sys.stdin)['username'])"`.
- After pushing a branch, the usual MR follow-up is:
  1. Find MR: `glab mr list --source-branch <branch>`.
  2. Assign: `glab mr update <id> --assignee <username>`.
  3. Update title if needed: `glab mr update <id> --title "PROJ-XXXXX: <description>"`.

### Merge Request Review

When asked to address MR comments:

1. Check the current branch with `git branch --show-current` and confirm it is the intended branch when uncertain.
2. Find the MR with `glab mr list --source-branch <branch>`.
3. Read comments with `glab mr view <mr-number> --comments`.
4. Present the comments and ask which ones to address when the request is ambiguous.
5. Address comments one at a time.
6. Verify each fix before committing, if commits are requested.
7. If committing review fixes, use a message that references the reviewer when useful, such as `Addresses review comment from <reviewer>`.

## Coding Instructions

1. Keep code clean and readable.
2. Avoid unnecessary complexity.
3. Use meaningful variable and function names.
4. Extract complex logic or calculations into named methods.
5. Write comments to explain complex logic.
6. Keep code well-structured and modular.
7. Follow the project's contribution guidelines.
8. Avoid hardcoded values when constants or configuration are more appropriate.
9. Follow SOLID principles where applicable.
10. Prefer fluent style when it improves readability.
11. Prefer parameterized tests over one-off tests when multiple cases are natural.
12. Use Given-When-Then structure for tests when it matches local style.
13. Run tests or other verification and inspect the result.
14. Prefer a single focused test over the full suite during implementation, then broaden verification when warranted.
15. Avoid generic production names like `data`, `result`, `obj`, and `item` when a domain-specific name is clearer.
16. Test-local variables may be shorter when clear.
17. Add comments only where the code is not self-explanatory.

### Scripts And Automation

When creating automation:

- Include health checks and status monitoring.
- Add color-coded output for clarity.
- Include safety confirmations for destructive actions.
- Provide clear help or usage text.
- Include both simple and advanced usage modes.
- Prefer feature-rich behavior over minimal implementations for explicitly requested "smart" scripts or automation.

## Java And Kotlin Rules

Applies to `**/*.java`, `**/*.kt`, and `**/*.kts`.

### Project Conventions

- Avoid `@Nullable` annotations unless the project already uses them.
- Avoid generic production variable names like `data`, `result`, `obj`, and `item`; use domain-specific names.
- Test-local variables may be shorter when clear.

### Java Style

1. Prefer `final` and `var` when consistent with the local codebase.
2. Prefer records for simple data carriers.
3. Use a single early return with `||` for multiple skip conditions when readable.
4. Prefer `Optional.ofNullable(x).map(...).orElse(null)` over multi-step null guards when it is clearer.

### Mockito And JUnit 5

1. Use `@ExtendWith(MockitoExtension.class)` at class level.
2. Use `@Mock` annotations on method parameters for test-specific mocks.
3. Use `@InjectMocks` for the class under test as a field.
4. Name tests as `test_methodName_condition_expectedResult` when the project has no stronger convention.
5. Use Given-When-Then comments for structure when helpful.
6. Avoid `lenient()`; remove unused stubs instead.
7. Stub only methods actually invoked during test execution.
8. Prefer `@Mock` parameters even for simple objects that do not need stubbing when that matches local style.
9. Prefer literal values in tests over static constants.
10. Use `Month.JANUARY` instead of numeric month values.
11. Use `.hasFieldOrPropertyWithValue()` for detailed error assertions.
12. For "does not throw" tests, call the method directly instead of using `assertThatCode`.

### MockK And JUnit 5

1. Use `@ExtendWith(MockKExtension::class)` at class level.
2. Use `@MockK` annotations for mocked dependencies.
3. Use `@InjectMockKs` for the class under test.
4. Use Given-When-Then comments for structure when helpful.

## Workflow Rules

### Implementation

- Break substantial work into ordered tasks.
- Keep one task in progress at a time.
- Run the narrowest useful tests during implementation.
- Run broader checks before final delivery when the change warrants it.
- Integration tests and BDD can be done after focused implementation tasks complete.

### Local Infrastructure

When local development infrastructure or UAT tests are requested, inspect project docs first, then start the needed 
local stack autonomously when safe. If the project still has a `CLAUDE.md` or `AGENTS.MD`, read it for local stack 
instructions.

## ASCII Diagram Guidelines

For sequence-style ASCII diagrams, every `|` present on a line must land on a target column defined by the header pipe row.

Verification helper:

```bash
sed -n 'START,ENDp' file | awk '{printf "%3d: ", NR+START-1; for(i=1;i<=length($0);i++){if(substr($0,i,1)=="|")printf "%d ",i};print ""}'
```

Rules:

1. Target columns come from the first `|...|` row, for example `4 22 42 56 71`.
2. Arrow lines may omit intermediate pipes when text overflows.
3. Arrow endpoints such as `>|` and `|<---` must land on target columns.
4. Check output against header pipe positions; a diagram is not done until all present pipes match.
5. The last column is the most common misalignment; count spaces carefully.
6. Fix one shifted pipe carefully because changes affect pipes to its right.

Fixing misalignments:

- Off by `+1`, such as `55` instead of `56`: remove one character before that `|`, usually a trailing space or dash.
- Off by `-1`, such as `57` instead of `56`: add one character before that `|`.
- Cascade: fixing a `|` shifts all pipes to its right on the same line; compensate if those were already correct.
- Long arrows: `|<` + N dashes + `|`, where N is `target_col - source_col - 2`.

## Key Commands

- `./gradlew spotlessApply` - format Gradle projects that use Spotless; run before `git add` when Spotless is part of the project workflow.
- `./gradlew clean spotlessApply test --tests "com.your.package.YourTestClass"` - run one test class with formatting.
- `./gradlew test --tests "com.your.package.YourTestClass.test_method"` - run one test method.
- `./gradlew clean spotlessApply test` - full Gradle verification for projects that use Spotless.
