from typing import List

from sym.flow.cli.errors import SymAPIRequestError
from sym.flow.cli.helpers.sym_api_client import BaseSymAPIClient


class SymAPIService:
    def __init__(self, api_client: BaseSymAPIClient):
        self.api_client = api_client

    def get_integration_table_data(self) -> List[List[str]]:
        integration_data, request_id = self.api_client.get_integrations()

        try:
            data = []
            for i in integration_data:
                updated_at = i["updated_at"].strftime("%d %b %Y %I:%M%p")
                data.append([i["name"], i["type"], updated_at])

            return data
        except KeyError:
            raise SymAPIRequestError(
                "failed to parse data received from the Sym API", request_id
            )
