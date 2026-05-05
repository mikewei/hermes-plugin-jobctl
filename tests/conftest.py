from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_SPEC = REPO_ROOT / "examples" / "sample-cron-task.md"


@pytest.fixture
def repo_root():
    return REPO_ROOT


@pytest.fixture
def example_spec_path():
    return EXAMPLE_SPEC
