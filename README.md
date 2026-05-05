# hermes-job

Declarative Hermes cron jobs from Markdown files: YAML **front matter** for metadata and a Markdown **body** as the Hermes agent prompt—think apply/delete/status for cron specs.

## Requirements

- Python 3.10+
- The `hermes` CLI on `PATH`, or override with **`HERMES_JOB_HERMES_BIN`**

---

## Installation

### From PyPI

```bash
pip install hermes-job
```

### From source

#### With [uv](https://docs.astral.sh/uv/)

From a **checkout** of this repository:

```bash
cd /path/to/hermes-job
uv sync
```

Run the CLI via the managed environment:

```bash
uv run hermes-job --help
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

---

## Quick Start

After installation, `hermes-job` must be on your `PATH` (or use `uv run hermes-job` from the project directory).

```bash
# Scaffold a spec next to cwd
hermes-job new nightly-report --schedule "every 24h" --dir .

# Edit nightly-report.md: set YAML header and write the Markdown prompt body

# Push spec to Hermes cron
hermes-job apply ./nightly-report.md

# See sync state vs jobs.json
hermes-job status ./nightly-report.md
```

Notes:

- You can pass **multiple** paths; each argument may be a `.md` file or a directory (every `*.md` in that directory, non-recursive).
- See **`Spec format`** at the bottom of **`hermes-job --help`** for the full field list.

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
hermes-job apply ./examples/sample-cron-task.md
hermes-job status ./examples/
hermes-job delete ./examples/sample-cron-task.md
hermes-job delete --name my-job
hermes-job new my-task --schedule "every 24h"
```

---

## Profile resolution

Resolution order for which Hermes home / `jobs.json` is used:

1. CLI `--profile` (`default` → unnamed profile)
2. Environment variable **`HERMES_JOB_PROFILE`**
3. If `cwd` is under `~/.hermes/profiles/<name>/…`, infer `<name>`

Each run prints a short line on stderr, e.g. `profile: default`.

---

## Development

```bash
uv sync --extra dev && uv run pytest
# or: pip install -e '.[dev]' && pytest
```

---

*Distribution name **`hermes-job`** in `pyproject.toml` `[project]`; console entry point **`hermes-job`**.*
