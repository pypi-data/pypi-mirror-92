from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from urllib.parse import quote
from uuid import uuid4

import requests
from dateutil.parser import isoparse

from sym.flow.cli.errors import (
    NotAuthorizedError,
    SymAPIMissingEntityError,
    SymAPIUnknownError,
    UnknownOrgError,
)
from sym.flow.cli.helpers.config import Config
from sym.flow.cli.models import Organization


class BaseSymAPIClient(ABC):
    @abstractmethod
    def get_integrations(self) -> Tuple[List[dict], str]:
        pass


class SymAPIClient(BaseSymAPIClient):
    def __init__(self, url: str):
        self.base_url = url

        try:
            self.access_token = Config.get_access_token()
        except KeyError:
            self.access_token = None

    def generate_header(self, auth_required: Optional[bool] = True) -> dict:
        if auth_required and not self.access_token:
            raise NotAuthorizedError

        headers = {"X-Sym-Request-ID": str(uuid4())}

        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"

        return headers

    def validate_response(self, response: requests.Response, request_id: str) -> None:
        if not response.ok:
            for Err in [SymAPIMissingEntityError]:
                if response.status_code in Err.error_codes:
                    raise Err(response_code=response.status_code, request_id=request_id)
            raise SymAPIUnknownError(
                response_code=response.status_code,
                request_id=request_id,
            )

    def get(
        self,
        endpoint: str,
        params: Optional[dict] = None,
        validate: Optional[bool] = True,
        auth_required: Optional[bool] = True,
    ) -> Tuple[requests.Response, str]:
        """Perform a GET request to the Sym API.

        Returns a tuple of (Response, Request ID) so the Request ID
        can be logged if any errors occur.
        """

        if params is None:
            params = {}

        headers = self.generate_header(auth_required=auth_required)
        response = requests.get(
            f"{self.base_url}/{endpoint}", params=params, headers=headers
        )

        if validate:
            self.validate_response(response, headers["X-Sym-Request-ID"])

        return response, headers["X-Sym-Request-ID"]

    def get_organization_from_email(self, email: str) -> Organization:
        """Exchanges the provided email for the corresponding Organization data."""

        try:
            response, _ = self.get(
                f"organizations/from-email/{quote(email)}",
                auth_required=False,
            )
            response_json = response.json()
            return Organization(
                slug=response_json["slug"], client_id=response_json["client_id"]
            )
        except KeyError:
            raise UnknownOrgError(email)

    def verify_login(self, email: str) -> bool:
        """Verifies Auth0 login was successful and the access token received
        will be respected by the Sym API.

        Returns True if login has been verified.
        """

        response, _ = self.get(f"verify-login/{quote(email)}")
        return response.status_code == 200

    def get_integrations(self) -> Tuple[List[dict], str]:
        """Retrieve all Sym Integrations accessible to the currently
        authenticated user.

        Converts retrieved Integrations' updated_at string to a datetime object
        with the local timezone.

        Returns the list of integration data as well as the Request ID for tracking.
        """

        response, request_id = self.get("integrations/search")
        integrations = []
        for integration in response.json():
            integration["updated_at"] = isoparse(integration["updated_at"]).astimezone()
            integrations.append(integration)
        return integrations, request_id

    def get_slack_install_url(self, integration_name: str) -> Tuple[str, str]:
        """Get the URL that starts the Slack App install flow."""

        response, request_id = self.get(
            "install/slack", params={"integration_name": integration_name}
        )
        return response.url, request_id

    def uninstall_slack(self, integration_name: str) -> str:
        """Make a request to the Sym API to uninstall the Slack App.

        Raises exception from validate_response on failure. Otherwise,
        assume success.
        """

        _, request_id = self.get(
            "uninstall/slack", params={"integration_name": integration_name}
        )
        return request_id
