import pytest
from cookiecutter_science_project_demo_repo.dummy import dummy_foo


def test_dummy():
    assert dummy_foo(4) == (4 + 4)
