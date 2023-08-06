from contextlib import contextmanager
from pathlib import Path
from typing import Optional

import pytest
from click.testing import CliRunner
from requests import Response
from sym.cli.tests.helpers.sandbox import Sandbox

from sym.flow.cli.models import Organization


@pytest.fixture
def click_setup(sandbox):
    @contextmanager
    def context():
        runner = CliRunner()
        with runner.isolated_filesystem():
            with sandbox.push_xdg_config_home():
                yield runner

    return context


@pytest.fixture
def sandbox(tmp_path: Path) -> Sandbox:
    return Sandbox(tmp_path)


@pytest.fixture
def test_org() -> Organization:
    return Organization(slug="test", client_id="12345abc")


class MockResponse(Response):
    def __init__(self, data: Optional[dict] = None):
        super().__init__()

        if data is None:
            data = {}

        self.data = data

    def json(self):
        return self.data


def get_mock_response(status_code: int, data: Optional[dict] = None) -> Response:
    response = MockResponse(data)
    response.status_code = status_code
    return response
