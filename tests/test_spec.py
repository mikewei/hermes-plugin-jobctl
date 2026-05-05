import pytest

from hermes_job.spec import TaskSpecError, parse_task_file, parse_task_text


def test_example_spec_parses(example_spec_path):
    s = parse_task_file(example_spec_path)
    assert s.task_type == "hermes-cron"
    assert s.effective_name == "sample-cron-task"
    assert "every 24h" in s.schedule
    assert s.deliver == "local"
    assert s.suspend is False
    assert s.skills == ()
    assert "Example scheduled task" in s.prompt_body


def test_name_override_in_header(tmp_path):
    p = tmp_path / "ignored-stem.md"
    p.write_text(
        """---
type: hermes-cron
schedule: "30m"
name: my-real-name
---
Do the thing.
""",
        encoding="utf-8",
    )
    s = parse_task_file(p)
    assert s.effective_name == "my-real-name"


def test_missing_front_matter_closing(tmp_path):
    p = tmp_path / "bad.md"
    p.write_text(
        """---
type: hermes-cron
schedule: "1h"
oops no close
""",
        encoding="utf-8",
    )
    with pytest.raises(TaskSpecError, match="closing"):
        parse_task_file(p)


def test_empty_body_rejected(tmp_path):
    p = tmp_path / "empty.md"
    p.write_text(
        """---
type: hermes-cron
schedule: "1h"
---
""",
        encoding="utf-8",
    )
    with pytest.raises(TaskSpecError, match="non-empty"):
        parse_task_file(p)


def test_missing_type_rejected(tmp_path):
    p = tmp_path / "no-type.md"
    p.write_text(
        """---
schedule: "1h"
---
Hi
""",
        encoding="utf-8",
    )
    with pytest.raises(TaskSpecError, match="`type` is required"):
        parse_task_file(p)


def test_unknown_type_rejected(tmp_path):
    p = tmp_path / "bad-type.md"
    p.write_text(
        """---
type: other-kind
schedule: "1h"
---
Hi
""",
        encoding="utf-8",
    )
    with pytest.raises(TaskSpecError, match=r"`type` must be one of"):
        parse_task_file(p)
