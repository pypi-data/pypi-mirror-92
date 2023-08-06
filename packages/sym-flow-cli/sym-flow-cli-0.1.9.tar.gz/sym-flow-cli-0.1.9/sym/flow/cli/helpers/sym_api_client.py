from typing import Optional
from urllib.parse import quote
from uuid import uuid4

import requests

from sym.flow.cli.errors import SymAPIUnknownError, UnknownOrgError
from sym.flow.cli.models import Organization


class SymAPIClient:
    def __init__(self, url: str, access_token: Optional[str] = None):
        self.base_url = url
        self.access_token = access_token

    def generate_header(self) -> dict:
        headers = {"X-Sym-Request-ID": str(uuid4())}

        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"

        return headers

    def validate_response(self, response: requests.Response, request_id: str) -> None:
        if not response.ok:
            raise SymAPIUnknownError(
                response_code=response.status_code, request_id=request_id
            )

    def get(
        self,
        endpoint: str,
        params: Optional[dict] = None,
        validate: Optional[bool] = True,
    ) -> requests.Response:
        if params is None:
            params = {}

        headers = self.generate_header()
        response = requests.get(
            f"{self.base_url}/{endpoint}/", params=params, headers=headers
        )

        if validate:
            self.validate_response(response, headers["X-Sym-Request-ID"])

        return response

    def get_organization_from_email(self, email: str) -> Organization:
        """Exchanges the provided email for the corresponding Organization data."""

        try:
            response = self.get(f"organizations/from-email/{email}")
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

        response = self.get(f"verify-login/{quote(email)}")
        return response.status_code == 200
