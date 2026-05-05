from __future__ import annotations

import sys
from pathlib import Path
from typing import Annotated, Optional

import typer

from hermes_task import __version__
from hermes_task.commands import apply_paths, delete_name_or_file, get_cmd, status_paths

app = typer.Typer(
    no_args_is_help=True,
    help=(
        "Declarative Hermes cron tasks from Markdown + YAML front matter. "
        "Example spec: examples/sample-cron-task.md"
    ),
)


@app.command()
def apply(
    file: Annotated[
        list[Path],
        typer.Option(
            "--file",
            "-f",
            exists=True,
            readable=True,
            help="Markdown task file or directory of *.md (non-recursive). Repeatable.",
        ),
    ] = [],
    profile: Optional[str] = typer.Option(None, "--profile", "-p"),
    hermes_bin: Optional[str] = typer.Option(None, "--hermes-bin", envvar="HERMES_TASK_HERMES_BIN"),
    accept_hooks: bool = typer.Option(False, "--accept-hooks"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
):
    """Create or update Hermes cron jobs from task spec files."""
    if not file:
        print("error: provide at least one -f/--file", file=sys.stderr)
        raise typer.Exit(2)
    code = apply_paths(file, profile_opt=profile, hermes_bin=hermes_bin, accept_hooks=accept_hooks, verbose=verbose)
    raise typer.Exit(code)


@app.command()
def delete(
    file: Optional[Path] = typer.Option(None, "--file", "-f", help="Task .md (uses its effective name)."),
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Effective task / job name."),
    profile: Optional[str] = typer.Option(None, "--profile", "-p"),
    hermes_bin: Optional[str] = typer.Option(None, "--hermes-bin", envvar="HERMES_TASK_HERMES_BIN"),
    accept_hooks: bool = typer.Option(False, "--accept-hooks"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
):
    """Remove a Hermes cron job by spec file or name."""
    try:
        code = delete_name_or_file(
            file,
            name,
            profile_opt=profile,
            hermes_bin=hermes_bin,
            accept_hooks=accept_hooks,
            verbose=verbose,
        )
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        raise typer.Exit(2) from e
    raise typer.Exit(code)


@app.command()
def status(
    file: Annotated[
        list[Path],
        typer.Option(
            "--file",
            "-f",
            exists=True,
            readable=True,
            help="Markdown task file or directory of *.md (non-recursive). Repeatable.",
        ),
    ] = [],
    profile: Optional[str] = typer.Option(None, "--profile", "-p"),
    hermes_bin: Optional[str] = typer.Option(None, "--hermes-bin", envvar="HERMES_TASK_HERMES_BIN"),
    json_out: bool = typer.Option(False, "--json", help="Print JSON rows."),
    show_diff: bool = typer.Option(False, "--show-diff", help="Extra hints when fields drift (use with -v)."),
    strict: bool = typer.Option(
        False,
        "--strict",
        help="Exit non-zero if any spec is invalid, missing job, drift, or ambiguous name.",
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
):
    """Compare task files to jobs.json (sync / pending_apply / missing)."""
    if not file:
        print("error: provide at least one -f/--file", file=sys.stderr)
        raise typer.Exit(2)
    code = status_paths(
        file,
        profile_opt=profile,
        hermes_bin=hermes_bin,
        json_out=json_out,
        show_diff=show_diff,
        strict=strict,
        verbose=verbose,
    )
    raise typer.Exit(code)


@app.command("get")
def get_jobs(
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Filter by job name (exact)."),
    profile: Optional[str] = typer.Option(None, "--profile", "-p"),
    hermes_bin: Optional[str] = typer.Option(None, "--hermes-bin", envvar="HERMES_TASK_HERMES_BIN"),
    json_out: bool = typer.Option(False, "--json"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
):
    """List jobs from jobs.json (optional name filter)."""
    code = get_cmd(
        name,
        profile_opt=profile,
        hermes_bin=hermes_bin,
        json_out=json_out,
        verbose=verbose,
    )
    raise typer.Exit(code)


def main() -> None:
    if len(sys.argv) >= 2 and sys.argv[1] in ("--version", "-V"):
        print(f"hermes-task {__version__}")
        raise SystemExit(0)
    app()


if __name__ == "__main__":
    main()
