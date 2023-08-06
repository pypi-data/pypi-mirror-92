from typing import List, Union

import httpx

from novaposhta.schemas.counterparties import (
    CounterpartyAddress, CounterpartyOptions, CounterpartyContactPerson,
    Counterparty as CounterpartySchema, ContactPerson as ContactPersonSchema,
    NewCounterparty, DeleteResponse,
    ThirdpartyBody, OrganizationBody, SenderBody, UpdateCounterpartyBody,
    CounterpartyContactPersonUpdateBody,
    CounterpartyContactPersonSaveBody
)
from .abstract import AbstractClient
from ..const import CounterpartyProperty

__all__ = (
    'Counterparty',
    'ContactPerson'
    # 'AsyncCounterparty'
)


class Counterparty(AbstractClient):
    MODEL = 'Counterparty'

    def get_addresses(
        self,
        ref: str,
        counterparty_property: CounterpartyProperty = CounterpartyProperty.SENDER
    ) -> List[CounterpartyAddress]:
        """
        Returns counterparty addresses
        :param ref: Counterparty ref.
        :param counterparty_property: Counterparty property to filter. Default `CounterpartyProperty.SENDER`
        :return: List of counterparty addresses
        """

        request = self.build_request(
            url=self.build_url('getCounterpartyAddresses'),
            json=self.build_params(
                'getCounterpartyAddresses',
                {'Ref': ref, 'CounterpartyProperty': counterparty_property.value}
            ),
            headers=self.get_headers()
        )
        response = self.make_request(request)

        return self.process_response(response, model=CounterpartyAddress)

    def get_options(self, ref: str) -> List[CounterpartyOptions]:
        """
        Returns counterparty options

        :param ref: Counterparty ref
        :return: List of counterparty options
        """
        request = self.build_request(
            url=self.build_url('getCounterpartyOptions'),
            json=self.build_params(
                'getCounterpartyOptions',
                {'Ref': ref}
            ),
            headers=self.get_headers()
        )

        response = self.make_request(request)

        return self.process_response(response, model=CounterpartyOptions)

    def get_contact_persons(self, ref: str, page: int = 1, limit: int = 5) -> List[CounterpartyContactPerson]:
        """
        Returns counterparty contact persons.

        :param ref: Counterparty ref
        :param page: Page to fetch.
        :param limit: Limit result records. Default: 5
        :return: List of counterparty contact persons
        """

        request = self.build_request(
            url=self.build_url('getCounterpartyContactPersons'),
            json=self.build_params(
                'getCounterpartyContactPersons',
                {'Ref': ref, 'Page': page, 'Limit': limit}
            ),
            headers=self.get_headers()
        )

        response = self.make_request(request)

        return self.process_response(response, model=CounterpartyContactPerson)

    def list(
        self,
        counterparty_property: str = 'Sender',
        find_by_string: str = None,
        page: int = 1,
        limit: int = 5,
    ) -> List[CounterpartySchema]:
        """
        Returns counterparties list

        :param counterparty_property: Filter counterparties by Sender/Recipient/ThirdPerson
        :param find_by_string: Search counterparty by name
        :param page: Page number to fetch. Default: 1
        :param limit: Limit number of records. Default: 5
        :return: List of counterparties
        """

        request = self.build_request(
            url=self.build_url('getCounterparties'),
            json=self.build_params(
                'getCounterparties',
                {
                    'CounterpartyProperty': counterparty_property,
                    'FindByString': find_by_string,
                    'Page': page,
                    'Limit': limit
                }
            ),
            headers=self.get_headers()
        )
        response = self.make_request(request)

        return self.process_response(response, model=CounterpartySchema)

    def update(self, body: UpdateCounterpartyBody) -> CounterpartySchema:
        """
        Update counterparty address.
        :param body: New counterparty data.
        :return: CounterpartySchema instance
        """

        request = self.build_request(
            url=self.build_url('update'),
            json=self.build_params(
                'update', body.dict(by_alias=True)
            ),
            headers=self.get_headers()
        )

        response = self.make_request(request)

        return self.process_response(response, model=CounterpartySchema, single=True)

    def save(self, body: Union[ThirdpartyBody, OrganizationBody, SenderBody]) -> NewCounterparty:
        """
        Saves new counterparty

        :param body: Counterparty data
        :return: Created counterparty
        """

        request = self.build_request(
            url=self.build_url('save'),
            json=self.build_params('save', body.dict(by_alias=True)),
            headers=self.get_headers()
        )
        response = self.make_request(request)

        return self.process_response(response, model=NewCounterparty, single=True)

    def delete(self, ref: str) -> DeleteResponse:
        """
        Deletes counterparty

        :param ref: Counterparty ref to delete
        :return: Deleted counterparty data
        """

        request = self.build_request(
            url=self.build_url('delete'),
            json=self.build_params(
                'delete',
                {"Ref": ref}
            ),
            headers=self.get_headers()
        )

        response = self.make_request(request)

        return self.process_response(response, model=DeleteResponse)


class ContactPerson(AbstractClient):
    MODEL = 'ContactPerson'

    def update(self, body: CounterpartyContactPersonUpdateBody):
        request = self.build_request(
            url=self.build_url('update'),
            json=self.build_params(
                'update', body.dict(by_alias=True)
            ),
            headers=self.get_headers()
        )

        response = self.make_request(request)

        return self.process_response(response, model=ContactPersonSchema, single=True)

    def save(self, body: CounterpartyContactPersonSaveBody) -> ContactPersonSchema:
        request = self.build_request(
            url=self.build_url('save'),
            json=self.build_params(
                'save', body.dict(by_alias=True)
            ),
            headers=self.get_headers()
        )

        response = self.make_request(request)

        return self.process_response(response, model=ContactPersonSchema, single=True)

    def delete(self, ref: str):
        request = self.build_request(
            url=self.build_url('delete'),
            json=self.build_params(
                'delete',
                {"Ref": ref}
            ),
            headers=self.get_headers()
        )

        response = self.make_request(request)

        return self.process_response(response, model=DeleteResponse, single=True)
