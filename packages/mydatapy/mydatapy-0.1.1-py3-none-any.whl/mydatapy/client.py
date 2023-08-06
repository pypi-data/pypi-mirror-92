from typing import Optional, Union

import requests
import xmltodict


class MyDataException(Exception):
    pass


class XmlValidationError(MyDataException):
    def __init__(self, errors: list) -> None:
        self.errors: list = errors

    def __str__(self) -> str:
        return str(self.errors)


class MyDataClient:
    """
    MyData API Wrapper
    The class wraps the mydata API to send and receive docs
    from the platform

    Params:
    -------------------------------------------------------
    user_id: str -> The id of the user on mydata.
    api_key: str -> The Ocp API Subscription key.
    base_url: str -> The base url of the mydata api. (defaults to dev)
    """
    def __init__(self, user_id: str, api_key: str, base_url: Optional[str] = None) -> None:
        self.user_id: str = user_id
        self.api_key: str = api_key
        self.base_url: str = base_url or "https://mydata-dev.azure-api.net"

    def call(self, endpoint: str, method: str = "GET", body: Optional[Union[dict, str]] = None,
             params: Optional[dict] = None) -> dict:
        """
        Abstract method to perform alls calls to my data api.
        """
        headers = {
            'aade-user-id': self.user_id,
            'Ocp-Apim-Subscription-Key': self.api_key
        }

        if isinstance(body, str):
            body = body.encode('utf-8')

        response = requests.request(
            method=method, url=f"{self.base_url}/{endpoint}", params=params, headers=headers,
            data=body
        )
        if not response.ok:
            raise ValueError(response.text)
        body = xmltodict.parse(response.text)
        if 'errors' in (result := body['ResponseDoc']['response']):
            raise XmlValidationError(result['errors'])
        return result

    def send_invoice(self, invoice: str):
        return self.call(
            method="POST", body=invoice, endpoint="SendInvoices"
        )
