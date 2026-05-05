import json

from pathlib import Path

from hermes_task.state import load_all_jobs


def test_load_jobs_empty_dict(tmp_path: Path):
    p = tmp_path / "jobs.json"
    p.write_text("{}", encoding="utf-8")
    assert load_all_jobs(p) == []


def test_load_jobs_legacy_jobs_key(tmp_path: Path):
    p = tmp_path / "jobs.json"
    payload = {"jobs": [{"id": "1", "name": "a"}]}
    p.write_text(json.dumps(payload), encoding="utf-8")
    assert len(load_all_jobs(p)) == 1
