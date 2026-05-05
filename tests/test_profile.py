from pathlib import Path

from hermes_job.profile import effective_hermes_home, infer_profile_from_cwd


def test_infer_profile_under_profiles(monkeypatch):
    home = Path("/home/user")
    profiles = home / ".hermes" / "profiles"
    monkeypatch.setattr(Path, "home", lambda: home)
    assert infer_profile_from_cwd(profiles.resolve()) is None  # exactly profiles root
    assert infer_profile_from_cwd((profiles / "abc").resolve()) == "abc"
    assert infer_profile_from_cwd((profiles / "abc" / "proj").resolve()) == "abc"


def test_effective_home_named(monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: Path("/home/user"))
    hh = effective_hermes_home("abc")
    assert hh == Path("/home/user/.hermes/profiles/abc").resolve()
