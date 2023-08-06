import urllib.parse

import boto3
import click
from sym.cli.decorators import require_bins, run_subprocess
from sym.cli.helpers.boto import intercept_boto_errors
from sym.cli.helpers.global_options import GlobalOptions
from sym.cli.helpers.updater import SymUpdater

from .symflow import symflow


@symflow.command(short_help="Upload Terraform output to Sym")
@click.argument(
    "tf_directory",
    type=click.Path(exists=True, file_okay=False),
    default=".",
)
@click.make_pass_decorator(GlobalOptions, ensure=True)
def upload_terraform_output(options: GlobalOptions, tf_directory) -> None:
    """Upload the output from Terraform in TF_DIRECTORY to Sym."""
    output = terraform_output(tf_directory, capture_output_=True)
    file_name = create_file_name(tf_directory)
    upload_to_s3(file_name, output[0])


@require_bins("terraform")
@run_subprocess
def terraform_output(directory: click.Path, **opts: str):
    yield ("terraform", f"-chdir={directory}", "output", "-json")


# Create a file name for the upload that includes the full directory path turned into hyphens so it
# is easy to find the right file
def create_file_name(tf_directory: str):
    dir_name = urllib.parse.quote(tf_directory).strip("/").replace("/", "-")
    return f"{dir_name}-output.json"


@intercept_boto_errors
def upload_to_s3(file_name: str, content: str):
    s3 = boto3.client(
        "s3",
        # Typically we don't include access keys like this, but are including write-only dropbox
        # keys here until we can generate temporary signed URLs via the API
        aws_access_key_id="AKIA23WDB56I6QOC4ZAR",
        aws_secret_access_key="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",
    )
    s3.put_object(
        ACL="bucket-owner-full-control",
        Body=content,
        Bucket="sym-dropbox-us-east-1",
        Key=file_name,
    )
