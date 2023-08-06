import webbrowser

import click
import requests
from sym.cli.errors import CliError

from sym.flow.cli.errors import NotAuthorizedError
from sym.flow.cli.helpers.login.token import get_auth_header

from ..helpers.global_options import GlobalOptions
from .symflow import symflow


@symflow.command(short_help="add Sym bot to Slack")
@click.option(
    "--integration-id",
    required=True,
    prompt="Slack Integration ID",
    help="Identifier for your Sym Slack Integration",
)
@click.make_pass_decorator(GlobalOptions, ensure=True)
def add_to_slack(options: GlobalOptions, integration_id: str) -> None:
    """Install the Sym Slack bot into your Slack workspace. Will open a
    browser window to confirm the installation.

    Run this command after performing a terraform apply to create your Sym Integrations.
    The outputs of that command will provide your Slack Integration ID.
    """

    initialize_slack_install(api_url=options.api_url, integration_id=integration_id)


def initialize_slack_install(api_url: str, integration_id: str):
    try:
        url = f"{api_url}/install/slack/"
        response = requests.get(
            url,
            headers={"Authorization": get_auth_header()},
            params={"integration_id": integration_id},
        )
        if response.ok:
            webbrowser.open(response.url)
        else:
            raise CliError(
                f"Sym API responded with a status code of {response.status_code}"
            )
    except NotAuthorizedError:
        raise
    except Exception as e:
        raise CliError(f"Unexpected error occurred during Slack installation: {e}")
