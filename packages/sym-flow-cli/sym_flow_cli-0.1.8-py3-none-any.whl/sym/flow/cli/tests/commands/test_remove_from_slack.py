from unittest.mock import patch

import pytest
from requests import Response
from sym.cli.errors import CliError
from sym.cli.helpers.config import Config

from sym.flow.cli.commands.remove_from_slack import slack_uninstall
from sym.flow.cli.errors import NotAuthorizedError
from sym.flow.cli.symflow import symflow as click_command


def get_mock_response(status_code: int):
    response = Response()
    response.status_code = status_code
    return response


class TestRemoveFromSlack:
    """Suite for testing Slack installation."""

    @patch("sym.flow.cli.commands.remove_from_slack.slack_uninstall")
    @patch("sym.flow.cli.commands.remove_from_slack.click.echo")
    def test_click_calls_uninstall_method_and_echoes(
        self, mock_click_echo, mock_slack_uninstall, click_setup
    ):
        with click_setup() as runner:
            result = runner.invoke(
                click_command, ["remove-from-slack", "--integration-id", "12345"]
            )
            assert result.exit_code == 0

        mock_slack_uninstall.assert_called_once()
        mock_click_echo.assert_called_once_with(
            "Uninstall successful! The Sym bot has been removed from your Slack workspace."
        )

    @patch("sym.flow.cli.commands.remove_from_slack.get_auth_header", return_value="")
    @patch("sym.flow.cli.commands.remove_from_slack.requests.get", return_value=0)
    def test_slack_uninstall_unknown_error_caught(
        self, mock_requests_get, mock_get_auth_header, sandbox
    ):
        with pytest.raises(CliError, match="Unexpected error occurred during Slack"):
            with sandbox.push_xdg_config_home():
                slack_uninstall("http://afakeurl.symops.io/", "12345")

        mock_requests_get.assert_called_once()
        mock_get_auth_header.assert_called_once()

    @patch("sym.flow.cli.commands.remove_from_slack.get_auth_header", return_value="")
    @patch(
        "sym.flow.cli.commands.remove_from_slack.requests.get",
        return_value=get_mock_response(302),
    )
    def test_good_response(self, mock_requests_get, mock_get_auth_header, sandbox):
        with sandbox.push_xdg_config_home():
            assert slack_uninstall("http://afakeurl.symops.io/", "12345") is None

        mock_requests_get.assert_called_once()
        mock_get_auth_header.assert_called_once()
