# Install Mimir

**Get Mimir, preview the project changes, apply the approved plan, and start Codex.** Project installation keeps the instructions with your code. Global installation makes shared guidance available to your Linux user.

[Overview](../README.md) · [First task](USAGE.md#first-session) · [How it works](HOW_IT_WORKS.md)

## Prerequisites

Run the installer in Bash on Linux or Windows Subsystem for Linux (WSL).

The installer and lifecycle tools need Bash 4.4+, Python 3.9+, Git, `jq`, and standard Linux tools such as `flock`, `sha256sum`, `timeout`, `find`, `sort`, and core utilities. Sign in to Codex in the app, IDE extension, or CLI you plan to use.

Check the main tools:

```bash
bash --version
python3 --version
git --version
jq --version
```

For Ubuntu or Debian, install the common system dependencies if missing:

```bash
sudo apt update
sudo apt install bash python3 git jq util-linux coreutils findutils
```

Use `sudo` only to install system packages. **Run Mimir as your normal user.**

## Get the source

Clone [Mimir](https://github.com/febshhy/mimir-codex) or extract its ZIP outside your application repository. Use `MIMIR_SRC` for the path to that directory.

```bash
MIMIR_SRC="/path/to/extracted/mimir-codex"
test -f "$MIMIR_SRC/AGENTS.md"
test -f "$MIMIR_SRC/scripts/mimir"
```

For a trusted Git source, use `scripts/mimir-bootstrap` with the reviewed commit pinned.

Use `MIMIR_SRC` in the same Bash session in the steps below.

## Choose a setup path

| Your situation | Next step |
| --- | --- |
| Existing team repository | [Existing project](#existing-project) |
| New application directory | [New project](#new-project) |
| Personal guidance shared across repositories | [Global installation](#global-installation) |

## Existing project

Work from the root of a **clean Git repository**. The first command writes a saved installation plan outside the application and leaves project files unchanged.

```bash
cd /path/to/your-project
git status --short
bash "$MIMIR_SRC/scripts/mimir" start --project . --integrate-agents
```

Review the planned changes, then apply and verify the installation.

```bash
bash "$MIMIR_SRC/scripts/mimir" start --project . --integrate-agents --apply
bash .mimir/install.sh --verify
git status --short  # includes new, untracked Mimir files
git diff --stat     # tracked changes only
```

`--integrate-agents` permits a bounded addition to existing `AGENTS.md` instructions. Setup rejects unmanaged-file collisions and stale or option-mismatched plans.

If the worktree contains changes, commit or stash them before preview. An explicit `--allow-dirty` exception is available, but requires careful review and the same option on preview and apply.

## New project

Choose a path that is absent or empty. Mimir can initialize Git and install its instructions.

```bash
mkdir -p "$HOME/projects"
bash "$MIMIR_SRC/scripts/mimir" start --project "$HOME/projects/my-app"
```

Review the plan, then apply and verify:

```bash
bash "$MIMIR_SRC/scripts/mimir" start --project "$HOME/projects/my-app" --apply
cd "$HOME/projects/my-app"
bash .mimir/install.sh --verify
```

Setup refuses unsafe nested repositories and populated directories without Git.

## Global installation

For shared user-level instructions instead of project-managed files:

```bash
bash "$MIMIR_SRC/install.sh" --global --integrate-agents --dry-run
bash "$MIMIR_SRC/install.sh" --global --integrate-agents
bash "$HOME/.local/share/mimir/release/install.sh" --global --verify
```

Review the preview before applying. The global installer uses the default Codex home directory.

## Start Codex

After installation, start a new Codex session in the target project.

- **Codex app:** Open the installed project folder and start a chat. [Desktop app guide](https://learn.chatgpt.com/docs/app)
- **IDE extension:** Open the installed project as your workspace and start a chat in the Codex panel. [IDE extension guide](https://learn.chatgpt.com/docs/codex/ide)
- **CLI:** Run `codex` from the project root. [Codex CLI](https://github.com/openai/codex)

For an existing codebase, Codex can use `$project-adoption`, `$software-design-thinking` and `$data-slicing` to inspect real application/data sources and trace relevant execution and lineage paths. [Start with a read-only task](USAGE.md#first-session).

## How Codex reads the installed guidance

The project installer adds a **short reference** to the active root `AGENTS.md` (or `AGENTS.override.md`) and installs the full Mimir coordinator guide at `.mimir/AGENTS.md`. Start a Mimir task with the following prompt.

> Read `.mimir/AGENTS.md` and the applicable skill documentation in `.agents/skills/`. Show the actual source evidence and the tests you plan to run. Do not invent contracts or claim unrun checks.

Project `.codex/config.toml` sets the coordinator model to `gpt-6.2-sol` with `high` effort and enables multi-agent tools. The reviewer profile uses `gpt-6.2-sol` with `high` effort and disables supported shell, app, plugin, memory, and permission-request capabilities; the routine profile uses `gpt-6-luna`. Resolve any conflict with an existing unmanaged `.codex/config.toml` before rerunning installation.

The tracked Mimir clone also sets `sandbox_mode = "workspace-write"`, `approval_policy = "on-request"`, and `approvals_reviewer = "auto_review"`. These approval defaults stay in the trusted clone. Installed target projects receive Mimir's model/routing files and agent profiles, while the installer omits those three approval keys from generated project config. This clone-scoped adaptation does not claim to match Heimdall's installer verbatim. Inspect and trust the project and its hooks before enabling them. In the Codex desktop app, choose **Approve for me** in the current chat where available.

The workflow assigns GPT-6.2 Sol to coordinate, decide material issues, independently review changes, and accept through the schema-3 factory gate. GPT-6 Luna performs routine edits, shell commands, tests, routine Git, and independent evidence collection. Every delegated WRITE starts a separate Luna evidence collection for Sol to review. Subagents start with fresh context (`fork_turns: none`) and a bounded A/E/R assignment. The configured PreToolUse hook uses the current model to check the Sol launcher and exact target profile/model pairing, and routes controlled command/edit/write tools to the Luna model. PreToolUse does not document a caller profile field. Fixtures cover these field checks; they do not verify live Codex hook execution or enforcement. Profile feature flags do not prove a live sandbox.

For notebook projects, run `python scripts/mimir-notebooks audit --root notebooks` in CI and register every generated `.ipynb` in a manifest.

## Verify, recover, or remove

Verify project installation at any time:

```bash
bash .mimir/install.sh --verify
```

If installation is interrupted, inspect the saved transaction and its recovery choices:

```bash
bash "$MIMIR_SRC/scripts/mimir" status --project /path/to/your-project
bash "$MIMIR_SRC/scripts/mimir" recover --project /path/to/your-project
```

After reviewing the state, request a recorded revert if needed:

```bash
bash "$MIMIR_SRC/scripts/mimir" recover --project /path/to/your-project --revert
```

Recovery preserves unfamiliar edits and may require manual resolution.

Remove a current installation when appropriate:

```bash
# From the application root:
bash .mimir/install.sh --remove

# Or, for a global installation:
bash "$HOME/.local/share/mimir/release/install.sh" --global --remove
```

Installation, verification, and removal do not modify or delete your application's `docs/` directory.

## Resolve setup problems

| Problem | Next step |
| --- | --- |
| Missing Git, Python, `jq`, or system utility | Install the named prerequisite and rerun the preview. |
| Source path already exists | Verify that the source path points to the Mimir files you intend to install. |
| `MIMIR_SRC` is unset | Set it to the downloaded source path in the current Bash session. |
| Wrong project directory | Check `git rev-parse --show-toplevel` and use the repository root. |
| Dirty worktree or existing instruction conflict | Preserve your changes, review the planned integration, and preview again. |
| Saved plan is stale | Regenerate and review the plan before applying. |
| Installation was interrupted | Use `status`, then inspect the reported recovery action. |
| Codex cannot find the guidance | Verify the installation and start a new Codex session in the intended repository. |

## Security and permissions

Grant Codex access to the resources it needs. Keep confidential credentials in a separate execution environment or behind a broker with scoped access. [Credential boundary](../docs/security/CREDENTIAL_BOUNDARY.md).

See the [data documentation templates](../docs/data/README.md).

## Optional Bend 2 proofs

For selected rules that justify formal verification, enable Bend 2 in both preview and apply:

```bash
bash "$MIMIR_SRC/scripts/mimir" start --project . --with-bend2
bash "$MIMIR_SRC/scripts/mimir" start --project . --with-bend2 --apply
```

Use a trusted Bend 2 executable. Approved `LAWS.bend` specify the selected formal behavior, while `PROOF.bend` supplies proof evidence for the model. Run conformance checks against the production implementation. [Read the proof workflow](../proofs/README.md).

**[Try a task](USAGE.md)** · [Understand the method](HOW_IT_WORKS.md) · [Back to Mimir](../README.md)
