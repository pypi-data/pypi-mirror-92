from typing import Dict, Type, TYPE_CHECKING, Optional
import logging

from httpx import Client, Response, Request, ConnectTimeout
from pydantic import BaseModel

from novaposhta.exceptions import InvalidDataError

if TYPE_CHECKING:  # pragma: no cover
    from novaposhta.client import AbstractNovaposhta


class AbstractClient():
    BASE_URL = 'https://api.novaposhta.ua/v2.0/json'
    MODEL = ''

    def __init__(self, client: 'AbstractNovaposhta', base_url: Optional[str] = None):
        self.client = client
        self.base_url = (base_url or self.BASE_URL).rstrip('/')

    def make_request(self, request: Request, retries: int = 5) -> Response:
        while retries > 0:
            try:
                return Client().send(request, timeout=3)
            except ConnectTimeout:
                retries -= 1
                continue

    def build_url(self, method: str):
        return f'{self.base_url}/{self.MODEL}/{method}'

    def build_params(self, method: str, properties: Optional[Dict] = None):
        if not properties:
            properties = {}

        return {
            "apiKey": self.client.api_key,
            "modelName": self.MODEL,
            "calledMethod": method,
            "methodProperties": {
                key: value for key, value in properties.items() if value is not None
            }
        }

    def get_headers(self):
        return {'Content-Type': 'application/json'}

    def build_request(
        self,
        url: str,
        json: Dict,
        headers: Dict,
        method: str = 'POST',
        **kwargs
    ) -> Request:
        headers = {
            **headers,
            **self.get_headers()
        }

        return Request(
            method=method,
            url=url,
            json=json,
            headers=headers,
            **kwargs
        )

    def process_response(
        self,
        response: Response,
        model: Type[BaseModel],
        key: Optional[str] = None,
        single: Optional[bool] = False
    ):
        response.raise_for_status()
        data = response.json()

        if data['errors']:
            raise InvalidDataError('Invalid addresses', data['errors'], data)

        if data['warnings']:
            logging.warning(data['warnings'])

        response_data = data['data']

        if key:
            response_data = response_data[0][key]

        data = [model(**x) for x in response_data]

        if single:
            return data[0]

        return data
