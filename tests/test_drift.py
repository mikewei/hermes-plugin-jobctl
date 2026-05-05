from hermes_task.drift import DesiredState, drift_fields, job_is_paused
from hermes_task.spec import parse_task_text


def sample_job():
    return {
        "id": "abc123",
        "name": "sample-cron-task",
        "prompt": "hello",
        "schedule_display": "every 24h",
        "schedule": {"kind": "interval"},
        "deliver": "local",
        "repeat": {"times": None, "completed": 0},
        "skills": [],
        "skill": None,
        "script": None,
        "workdir": None,
        "enabled": True,
        "state": "scheduled",
    }


def test_sync_no_drift(tmp_path):
    p = tmp_path / "t.md"
    text = """---
schedule: "every 24h"
deliver: local
suspend: false
---
hello
"""
    spec = parse_task_text(p, text)
    d = DesiredState(
        schedule=spec.schedule,
        prompt=spec.prompt_body,
        deliver=spec.deliver,
        repeat=spec.repeat,
        skills=spec.skills,
        script=spec.script,
        workdir=spec.workdir,
        suspend=spec.suspend,
    )
    assert drift_fields(d, sample_job()) == []


def test_prompt_drift():
    j = sample_job()
    j["prompt"] = "other"
    d = DesiredState(
        schedule="every 24h",
        prompt="hello",
        deliver="local",
        repeat=None,
        skills=(),
        script=None,
        workdir=None,
        suspend=False,
    )
    assert "prompt" in drift_fields(d, j)


def test_paused_mismatch():
    j = sample_job()
    j["state"] = "paused"
    j["enabled"] = False
    assert job_is_paused(j)
    d = DesiredState(
        schedule="every 24h",
        prompt="hello",
        deliver="local",
        repeat=None,
        skills=(),
        script=None,
        workdir=None,
        suspend=False,
    )
    assert "suspend" in drift_fields(d, j)
