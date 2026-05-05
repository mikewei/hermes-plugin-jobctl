from hermes_job.state import find_jobs_by_name, singleton_job_or_error


def test_singleton_ambiguous():
    jobs = [{"id": "1", "name": "x"}, {"id": "2", "name": "x"}]
    j, err = singleton_job_or_error(jobs, "x")
    assert j is None
    assert err and "multiple" in err


def test_singleton_one():
    jobs = [{"id": "9", "name": "only"}]
    j, err = singleton_job_or_error(jobs, "only")
    assert err is None
    assert j["id"] == "9"
