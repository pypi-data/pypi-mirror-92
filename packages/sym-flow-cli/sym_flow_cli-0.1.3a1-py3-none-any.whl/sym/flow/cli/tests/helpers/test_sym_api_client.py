from typing import Optional
from unittest.mock import ANY, patch
from urllib.parse import quote

import pytest

from sym.flow.cli.errors import SymAPIUnknownError, UnknownOrgError
from sym.flow.cli.helpers.sym_api_client import SymAPIClient
from sym.flow.cli.tests.conftest import get_mock_response


@pytest.fixture
def sym_api_client() -> SymAPIClient:
    return SymAPIClient(url="http://faketest.symops.io/api/v1", access_token="12345")


class TestSymAPIClient:
    def test_generate_header(self, sym_api_client):
        headers = sym_api_client.generate_header()
        assert headers.get("X-Sym-Request-ID") is not None
        assert headers.get("Authorization") == "Bearer 12345"

    def test_validate_response(self, sym_api_client):
        response_500 = get_mock_response(500)
        with pytest.raises(SymAPIUnknownError, match="500"):
            sym_api_client.validate_response(response_500, "abc")

        response_400 = get_mock_response(400)
        with pytest.raises(SymAPIUnknownError, match="400"):
            sym_api_client.validate_response(response_400, "abc")

        response_200 = get_mock_response(200)
        assert sym_api_client.validate_response(response_200, "abc") is None

    @patch(
        "sym.flow.cli.helpers.sym_api_client.requests.get",
        return_value=get_mock_response(200),
    )
    def test_get(self, mock_requests_get, sym_api_client):
        params = {"test": "hello"}
        sym_api_client.get("fake-endpoint", params=params)
        mock_requests_get.assert_called_once_with(
            "http://faketest.symops.io/api/v1/fake-endpoint/", params=params, headers=ANY
        )

    @patch(
        "sym.flow.cli.helpers.sym_api_client.SymAPIClient.get",
        return_value=get_mock_response(
            200, data={"client_id": "12345abc", "slug": "test"}
        ),
    )
    def test_get_organization_from_email(self, mock_api_get, sym_api_client, test_org):
        email = "test@symops.io"
        org = sym_api_client.get_organization_from_email(email)

        mock_api_get.assert_called_once_with(f"organizations/from-email/{email}")
        assert org == test_org

    @patch(
        "sym.flow.cli.helpers.sym_api_client.SymAPIClient.get",
        return_value=get_mock_response(200),
    )
    def test_get_organization_from_email_missing_data_errors(
        self, mock_api_get, sym_api_client, test_org
    ):
        email = "test@symops.io"

        with patch(
            "sym.flow.cli.helpers.sym_api_client.SymAPIClient.get",
            return_value=get_mock_response(200, data={"client_id": "123"}),
        ) as mock_api_get_missing_slug:
            with pytest.raises(
                UnknownOrgError, match=f"Unknown organization for email: {email}"
            ):
                org = sym_api_client.get_organization_from_email(email)

        with patch(
            "sym.flow.cli.helpers.sym_api_client.SymAPIClient.get",
            return_value=get_mock_response(200, data={"slug": "test"}),
        ) as mock_api_get_missing_client_id:
            with pytest.raises(
                UnknownOrgError, match=f"Unknown organization for email: {email}"
            ):
                org = sym_api_client.get_organization_from_email(email)

        mock_api_get_missing_slug.assert_called_once()
        mock_api_get_missing_client_id.assert_called_once()

    @pytest.mark.parametrize("status_code", [400, 403, 500])
    def test_verify_login_failure(self, status_code, sym_api_client):
        with patch(
            "sym.flow.cli.helpers.sym_api_client.SymAPIClient.get",
            return_value=get_mock_response(status_code),
        ) as mock_api_get:
            assert sym_api_client.verify_login("test@symops.io") is False
        mock_api_get.assert_called_once_with(f"verify-login/{quote('test@symops.io')}")

    @pytest.mark.parametrize("status_code", [200])
    def test_verify_login_success(self, status_code, sym_api_client):
        with patch(
            "sym.flow.cli.helpers.sym_api_client.SymAPIClient.get",
            return_value=get_mock_response(status_code),
        ) as mock_api_get:
            assert sym_api_client.verify_login("test@symops.io") is True
        mock_api_get.assert_called_once_with(f"verify-login/{quote('test@symops.io')}")
