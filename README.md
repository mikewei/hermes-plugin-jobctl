# hermes-jobctl

Declarative Hermes cron jobs from Markdown files: YAML **front matter** for metadata and a Markdown **body** as the Hermes agent prompt—think apply/delete/status for cron specs.

## Requirements

- Python 3.10+
- The `hermes` CLI on `PATH`, or override with **`HERMES_JOBCTL_HERMES_BIN`**

---

## Installation

### From PyPI

```bash
pip install hermes-jobctl
```

### From source

#### With [uv](https://docs.astral.sh/uv/)

From a **checkout** of this repository:

```bash
cd /path/to/hermes-jobctl
uv sync
```

Run the CLI via the managed environment:

```bash
uv run hermes-jobctl --help
```

Editable install still bound to your tree:

```bash
uv pip install -e .
```

#### With pip

Inside the repo:

```bash
pip install .
pip install -e '.[dev]'   # editable + dev deps
```

### Hermes plugin registration

`hermes-jobctl` supports two plugin-loading paths for `hermes jobctl ...`:

1. **Python entry point** (default when installed via `pip` / `uv`)
   - Declared under `hermes_agent.plugins` as `jobctl = "hermes_jobctl.plugin"`.
2. **Directory plugin loading**
   - Copy the `hermes_jobctl/` directory directly into your Hermes `plugins` directory.
   - The package root exports `register`, so Hermes can register the `jobctl` command tree from the copied directory.

---

## Quick Start

After installation, `hermes-jobctl` must be on your `PATH` (or use `uv run hermes-jobctl` from the project directory).

```bash
# Scaffold a spec next to cwd
hermes-jobctl new nightly-report --schedule "every 24h" --dir .

# Edit nightly-report.md: set YAML header and write the Markdown prompt body

# Push spec to Hermes cron
hermes-jobctl apply ./nightly-report.md

# See sync state vs jobs.json
hermes-jobctl status ./nightly-report.md
```

Notes:

- You can pass **multiple** paths; each argument may be a `.md` file or a directory (every `*.md` in that directory, non-recursive).
- See **`Spec format`** at the bottom of **`hermes-jobctl --help`** for the full field list.

---

## Front matter (YAML header)

Everything between the first `---` and the closing `---` is YAML. **Do not put the Hermes prompt in YAML**—put it below the closing `---` as Markdown.

| Field | Required | Description |
|-------|----------|-------------|
| `type` | yes | Task kind. Only **`hermes-cron`** is supported today (reserved for future kinds). |
| `schedule` | yes | Hermes cron schedule string (e.g. `30m`, `every 2h`, `0 9 * * *`). |
| `name` | no | Job name; default: filename without `.md`. |
| `deliver` | no | Passed to Hermes `--deliver`; omit for default. |
| `repeat` | no | Integer; omit or ≤0 → unlimited per Hermes rules. |
| `skills` | no | List or single string → multiple `--skill`. |
| `script` | no | Maps to `--script`. |
| `workdir` | no | Maps to `--workdir` (often absolute). |
| `suspend` | no | If true, apply then pause job to match (default false). |

Any other YAML keys are **ignored** (not forwarded to Hermes).

---

## Example spec file

Repository copy: [`examples/sample-cron-task.md`](examples/sample-cron-task.md).

```markdown
---
type: hermes-cron
schedule: "every 24h"
deliver: local
suspend: false
---

Example scheduled task for Hermes cron. Copy and edit as needed.

- Summarize open todos in three short sections.
- If anything is blocked, call it out in one line.

(No `skills` in this sample; add `skills: [your-skill]` in the YAML header if you need them.)
```

---

## Commands

| Command | Purpose |
|---------|---------|
| `apply PATHS…` | Create or update jobs from `.md` files and/or directories (non‑recursive `*.md` each). |
| `delete PATHS…` \| `delete --name NAME` | Remove a job by spec path(s) or by job name. |
| `status PATHS…` | Compare specs to `jobs.json` (sync / pending_apply / missing, etc.). |
| `get` | List jobs in `jobs.json` (optional `--name`, `--json`). |
| `new TASK` | Scaffold a starter spec (`--schedule`, `--dir` / `-o/--output`, `--stdout`, `--force`). |

Common flags: `-p/--profile`, `--hermes-bin`, `-v/--verbose`; `apply` / `delete` also support `--accept-hooks`.

```bash
hermes-jobctl apply ./examples/sample-cron-task.md
hermes-jobctl status ./examples/
hermes-jobctl delete ./examples/sample-cron-task.md
hermes-jobctl delete --name my-job
hermes-jobctl new my-task --schedule "every 24h"
```

---

## Profile resolution

Resolution order for which Hermes home / `jobs.json` is used:

1. CLI `--profile` (`default` → unnamed profile)
2. Environment variable **`HERMES_JOBCTL_PROFILE`**
3. If `cwd` is under `~/.hermes/profiles/<name>/…`, infer `<name>`

Each run prints a short line on stderr, e.g. `profile: default`.

---

## Development

```bash
uv sync --extra dev && uv run pytest
# or: pip install -e '.[dev]' && pytest
```

---

*Distribution name **`hermes-jobctl`** in `pyproject.toml` `[project]`; console entry point **`hermes-jobctl`**.*
