from typing import Optional, List

from novaposhta.schemas import (
    SearchAddress, SearchSettlementStreet, SaveAddress, DeleteAddress, Area,
    City, Settlement, Warehouse, Street, WarehouseType
)
from .abstract import AbstractClient

__all__ = (
    'Address',
)

from ..schemas.addresses import WarehouseFilter, AddressSaveBody, AddressUpdateBody


class Address(AbstractClient):
    MODEL = 'Address'

    def search_settlements(self, name: str, limit: int = 5) -> List[SearchAddress]:
        """
        Returns settlements list with a given settlement name

        :param name: Settlement name to search for.
        :param limit: Limit the output records. Default: 5
        :return: List of found settlements
        """
        request = self.build_request(
            url=self.build_url('searchSettlements'),
            json=self.build_params(
                'searchSettlements',
                {'CityName': name, 'Limit': limit}
            ),
            headers=self.get_headers()
        )

        response = self.make_request(request)
        return self.process_response(response, model=SearchAddress, key='Addresses')

    def search_settlement_streets(
        self,
        street_name: str,
        settlement_ref: str,
        limit: int = 5
    ) -> List[SearchSettlementStreet]:
        """
        Search streets in a given settlement.

        :param street_name: Street name to search
        :param settlement_ref: Settlement ref from novaposhta
        :param limit: Limit the output records. Default: 5
        :return: List of found streets
        """
        request = self.build_request(
            url=self.build_url('searchSettlementStreets'),
            json=self.build_params(
                'searchSettlementStreets',
                {
                    "StreetName": street_name,
                    "SettlementRef": settlement_ref,
                    "Limit": limit
                }
            ),
            headers=self.get_headers()
        )

        response = self.make_request(request)
        return self.process_response(response, model=SearchSettlementStreet, key='Addresses')

    def save(self, body: AddressSaveBody) -> SaveAddress:
        """
        Save counterparty delivery/sending address.
        If address was created already - returns it

        :param body: New address body.
        :return: Created address.
        """

        request = self.build_request(
            url=self.build_url('save'),
            json=self.build_params('save', body.dict(by_alias=True)),
            headers=self.get_headers()
        )

        response = self.make_request(request)

        return self.process_response(response, model=SaveAddress, single=True)

    def update(self, body: AddressUpdateBody) -> SaveAddress:
        """
        Update counterparty address details.

        :param body: New address body.
        :return: Updated address.
        """

        request = self.build_request(
            url=self.build_url('update'),
            json=self.build_params('update', body.dict(by_alias=True)),
            headers=self.get_headers()
        )
        response = self.make_request(request)

        return self.process_response(response, model=SaveAddress, single=True)

    def delete(self, ref: str) -> DeleteAddress:
        """
        Deletes counterparty address.

        :param ref: Counterparty address ref.
        :return: Deleted address ref
        """

        request = self.build_request(
            url=self.build_url('delete'),
            json=self.build_params(
                'delete', {"Ref": ref}
            ),
            headers=self.get_headers()
        )
        response = self.make_request(request)

        return self.process_response(response, model=DeleteAddress, single=True)

    def get_areas(self) -> List[Area]:
        """
        :return: List of areas
        """
        request = self.build_request(
            url=self.build_url('getAreas'),
            json=self.build_params('getAreas'),
            headers=self.get_headers()
        )
        response = self.make_request(request)

        return self.process_response(response, model=Area)

    def get_cities(
        self,
        ref: Optional[str] = None,
        find_by_string: Optional[str] = None,
        page: int = 1,
        limit: int = 5
    ) -> List[City]:
        """
        Returns cities with novaposhta warehouses

        :param ref: City ref.
        :param find_by_string: City name
        :param page: Page number to fetch. Default: 1
        :param limit: Limit the number of records. Default: 5
        :return: List of cities
        """

        request = self.build_request(
            url=self.build_url('getCities'),
            json=self.build_params('getCities', {
                'Ref': ref,
                'Page': page,
                'FindByString': find_by_string,
                'Limit': limit
            }),
            headers=self.get_headers()
        )
        response = self.make_request(request)

        return self.process_response(response, model=City)

    def get_settlements(
        self,
        ref: Optional[str] = None,
        region_ref: Optional[str] = None,
        area_ref: Optional[str] = None,
        find_by_string: Optional[str] = None,
        warehouse: int = 1,
        page: int = 1,
        limit: int = 5
    ) -> List[Settlement]:
        """
        Returns Ukraine settlements that supports novaposhta delivery.

        :param ref: Settlement ref.
        :param region_ref: Region ref.
        :param area_ref: Area ref.
        :param find_by_string: Find settlement by name.
        :param warehouse: Filters settlements by warehouse availability.
        :param page: Page to fetch. Default: 1.
        :param limit: Limit number of records. Default: 5.
        :return: List of settlements
        """
        request = self.build_request(
            url=self.build_url('getSettlements'),
            json=self.build_params('getSettlements', {
                'Ref': ref,
                'RegionRef': region_ref,
                'AreaRef': area_ref,
                'FindByString': find_by_string,
                "Warehouse": warehouse,
                'Page': page,
                'Limit': limit
            }),
            headers=self.get_headers()
        )
        response = self.make_request(request)

        return self.process_response(response, model=Settlement)

    def get_warehouses(
        self,
        filter: WarehouseFilter,
        page: int = 1,
        limit: int = 100
    ) -> List[Warehouse]:
        """
        Returns list of available warehouses.

        :param page: Page number to fetch. Default: 1
        :param limit: Limit records. Default: 5
        :param filter: Warehouses filter
        :return: Returns warehouses list
        """

        request = self.build_request(
            url=self.build_url('getWarehouses'),
            json=self.build_params('getWarehouses', {
                'Page': page,
                'Limit': limit,
                **filter.dict(by_alias=True)
            }),
            headers=self.get_headers()
        )

        response = self.make_request(request)

        return self.process_response(response, model=Warehouse)

    def get_warehouse_types(self) -> List[WarehouseType]:
        """
        :return: Returns warehouses list
        :rtype: List[WarehouseType]
        """

        request = self.build_request(
            url=self.build_url('getWarehouseTypes'),
            json=self.build_params('getWarehouseTypes', {}),
            headers=self.get_headers()
        )
        response = self.make_request(request)

        return self.process_response(response, model=WarehouseType)

    def get_city_streets(
        self,
        city_ref: str,
        find_by_string: Optional[str] = None,
        page: int = 1,
        limit: int = 5
    ) -> List[Street]:
        """
        Returns city streets that supports delivery.

        :param city_ref: City ref.
        :param find_by_string: Street name to search.
        :param page: Page number to fetch.
        :param limit: Limit number of records per page.
        :return: List of city streets
        """
        request = self.build_request(
            url=self.build_url('getStreet'),
            json=self.build_params('getStreet', {
                'CityRef': city_ref,
                'FindByString': find_by_string,
                'Page': page,
                'Limit': limit
            }),
            headers=self.get_headers()
        )
        response = self.make_request(request)

        return self.process_response(response, model=Street)
