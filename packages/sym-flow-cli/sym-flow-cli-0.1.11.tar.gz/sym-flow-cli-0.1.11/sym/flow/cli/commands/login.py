import click
import validators

from sym.flow.cli.errors import SymAPIUnknownError
from sym.flow.cli.helpers.config import store_login_config
from sym.flow.cli.helpers.login.login_flow import LoginFlow
from sym.flow.cli.helpers.sym_api_client import SymAPIClient

from ..helpers.global_options import GlobalOptions
from .symflow import symflow


def validate_email(ctx, param, value):
    if value and not validators.email(value):
        raise click.BadParameter("must enter a valid email address")
    return value


@symflow.command(short_help="Log in to your Sym account", hidden=True)
@click.make_pass_decorator(GlobalOptions, ensure=True)
@click.option(
    "--browser/--no-browser",
    default=True,
    is_flag=True,
)
@click.option(
    "--port",
    default=11001,
)
@click.option(
    "--email",
    callback=validate_email,
    prompt=True,
)
def login(options: GlobalOptions, browser: bool, port: int, email: str) -> None:
    api_client = SymAPIClient(url=options.api_url)
    org = api_client.get_organization_from_email(email)
    click.echo("Successfully loaded org: {slug} ({client_id})".format(**org))

    auth_token = LoginFlow.get_login_flow(email, browser, port).login(options, org)
    api_client.access_token = auth_token.get("access_token")
    fail_msg = "Sym could not verify this login. Please try again, or visit https://docs.symops.com/docs/login-sym-flow for more details."

    try:
        login_success = api_client.verify_login(email)
        if not login_success:
            click.echo(fail_msg)
            return
    except SymAPIUnknownError:
        click.echo(fail_msg)
        return

    options.dprint(auth_token=auth_token)
    click.echo("Login succeeded")

    file = store_login_config(email, org, auth_token)
