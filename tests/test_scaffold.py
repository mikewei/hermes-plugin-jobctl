import io
from contextlib import redirect_stdout
from pathlib import Path

import pytest

from hermes_job.scaffold import render_spec_template, run_new, validate_task_stem
from hermes_job.spec import parse_task_file


def test_validate_rejects_empty():
    with pytest.raises(ValueError):
        validate_task_stem("  ")


def test_validate_strips_md_suffix():
    assert validate_task_stem("foo.md") == "foo"


def test_template_contains_keys():
    t = render_spec_template(stem="demo", schedule="1h")
    assert "type: hermes-cron" in t
    assert 'schedule: "1h"' in t
    assert "deliver" in t
    assert "suspend" in t
    assert t.startswith("---")


def test_run_new_writes(tmp_path):
    code = run_new(
        "alpha",
        directory=tmp_path,
        output=None,
        schedule="30m",
        force=False,
        stdout_flag=False,
    )
    assert code == 0
    p = tmp_path / "alpha.md"
    assert p.is_file()
    assert "30m" in p.read_text(encoding="utf-8")

    assert (
        run_new(
            "alpha",
            directory=tmp_path,
            output=None,
            schedule="30m",
            force=False,
            stdout_flag=False,
        )
        == 1
    )
    assert (
        run_new(
            "alpha",
            directory=tmp_path,
            output=None,
            schedule="30m",
            force=True,
            stdout_flag=False,
        )
        == 0
    )


def test_stdout(tmp_path):
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = run_new(
            "beta",
            directory=None,
            output=None,
            schedule="every 2h",
            force=False,
            stdout_flag=True,
        )
    assert code == 0
    assert "every 2h" in buf.getvalue()
    assert not (tmp_path / "beta.md").exists()


def test_new_file_parses(tmp_path):
    run_new("parsed", directory=tmp_path, output=None, schedule="5m", force=False, stdout_flag=False)
    spec = parse_task_file(tmp_path / "parsed.md")
    assert spec.effective_name == "parsed"
    assert spec.schedule == "5m"


def test_dir_and_output_conflict():
    code = run_new(
        "x",
        directory=Path("/tmp"),
        output=Path("/tmp/y.md"),
        schedule="1h",
        force=False,
        stdout_flag=False,
    )
    assert code == 2


def test_output_path_stem_in_comment(tmp_path):
    sub = tmp_path / "out"
    sub.mkdir()
    target = sub / "gamma.md"
    code = run_new(
        "ignored-stem",
        directory=None,
        output=target,
        schedule="1h",
        force=False,
        stdout_flag=False,
    )
    assert code == 0
    assert "'gamma'" in target.read_text(encoding="utf-8")
