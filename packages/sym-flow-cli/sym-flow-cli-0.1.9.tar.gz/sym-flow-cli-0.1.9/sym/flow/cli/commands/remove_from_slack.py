import webbrowser

import click
import requests
from sym.cli.errors import CliError

from sym.flow.cli.errors import NotAuthorizedError
from sym.flow.cli.helpers.login.token import get_auth_header

from ..helpers.global_options import GlobalOptions
from .symflow import symflow


@symflow.command(short_help="remove Sym bot from Slack")
@click.option(
    "--integration-id",
    required=True,
    prompt="Slack Integration ID",
    help="Identifier for your Sym Slack Integration",
)
@click.make_pass_decorator(GlobalOptions, ensure=True)
def remove_from_slack(options: GlobalOptions, integration_id: str) -> None:
    """Remove the Sym Slack bot from your Slack workspace."""

    slack_uninstall(api_url=options.api_url, integration_id=integration_id)
    click.echo(
        "Uninstall successful! The Sym bot has been removed from your Slack workspace."
    )


def slack_uninstall(api_url: str, integration_id: str):
    try:
        url = f"{api_url}/uninstall/slack/"
        response = requests.get(
            url,
            headers={"Authorization": get_auth_header()},
            params={"integration_id": integration_id},
        )
        if not response.ok:
            raise CliError(
                f"Sym API responded with a status code of {response.status_code}"
            )
    except NotAuthorizedError:
        raise
    except Exception as e:
        raise CliError(f"Unexpected error occurred during Slack uninstallation: {e}")
