from unittest.mock import patch

from hermes_job.hermes_runner import build_create_args, build_edit_args
from hermes_job.profile import build_cron_context
from hermes_job.spec import parse_task_text
from pathlib import Path


def test_build_cron_context_default():
    def fake_which(name):
        if str(name) == "/opt/hermes":
            return "/opt/hermes"
        return None

    with patch("hermes_job.profile.shutil.which", side_effect=fake_which):
        ctx = build_cron_context(None, hermes_bin="/opt/hermes")
    assert ctx.argv_prefix == ("/opt/hermes", "cron")


def test_build_cron_context_named_fallback():
    def fake_which(name):
        name = str(name)
        if name == "myprofile":
            return None
        if name == "/bin/hermes":
            return "/bin/hermes"
        return None

    with patch("hermes_job.profile.shutil.which", side_effect=fake_which):
        ctx = build_cron_context("myprofile", hermes_bin="/bin/hermes")
        assert ctx.argv_prefix == ("/bin/hermes", "-p", "myprofile", "cron")


def test_build_cron_context_named_wrapper():
    def fake_which(name):
        name = str(name)
        if name == "myprofile":
            return f"/home/u/.local/bin/{name}"
        if name.endswith("hermes"):
            return "/bin/hermes"
        return None

    with patch("hermes_job.profile.shutil.which", side_effect=fake_which):
        ctx = build_cron_context("myprofile", hermes_bin="/bin/hermes")
        assert ctx.argv_prefix == ("myprofile", "cron")


def test_create_argv(tmp_path):
    p = tmp_path / "z.md"
    spec = parse_task_text(
        p,
        """---
type: hermes-cron
schedule: "1h"
deliver: local
skills: [a, b]
---
x
""",
    )
    args = build_create_args(spec)
    assert args[0] == "create"
    assert "1h" in args
    assert "x" in args
    assert "--skill" in args
    assert args.count("--skill") == 2
