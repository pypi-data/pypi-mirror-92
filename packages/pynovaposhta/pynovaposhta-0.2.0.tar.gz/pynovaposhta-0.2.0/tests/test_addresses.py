from typing import TYPE_CHECKING

import pytest

from novaposhta.schemas import (
    SearchAddress, SearchSettlementStreet, Area, WarehouseType, WarehouseFilter,
    Street, AddressSaveBody, AddressUpdateBody
)
from novaposhta.exceptions import InvalidDataError

if TYPE_CHECKING:  # pragma: no cover
    from novaposhta.client import Novaposhta


def test_search_settlements(client: 'Novaposhta'):
    settlements = client.addresses().search_settlements('Киев')
    assert len(settlements) == 5

    limit = 2
    settlements = client.addresses().search_settlements('Киев', limit=limit)
    assert len(settlements) == limit
    assert type(settlements[0]) == SearchAddress

    # Invalid data
    limit = 200000

    with pytest.raises(InvalidDataError):
        client.addresses().search_settlements('Киев', limit=limit)


def test_search_settlement_streets(client: 'Novaposhta'):
    settlement = client.addresses().search_settlements('Киев')[0]

    limit = 3
    settlements = client.addresses().search_settlement_streets('Хрещ', settlement_ref=settlement.ref, limit=limit)
    assert len(settlements) <= limit
    assert type(settlements[0]) == SearchSettlementStreet

    # Invalid data
    limit = 200000

    with pytest.raises(InvalidDataError):
        client.addresses().search_settlement_streets('Хрещ', settlement_ref=settlement.ref, limit=limit)


def test_get_areas(client: 'Novaposhta'):
    areas = client.addresses().get_areas()
    assert len(areas) > 1
    assert type(areas[0]) == Area


def test_get_cities(client: 'Novaposhta'):
    limit = 3
    cities = client.addresses().get_cities(limit=limit)
    assert len(cities) == 3

    second_page = client.addresses().get_cities(page=2, limit=limit)
    assert len(cities) == 3
    assert cities != second_page

    cities = client.addresses().get_cities(find_by_string='Киев', limit=limit)
    assert len(cities) == 2

    cities = client.addresses().get_cities(ref=cities[0].ref)
    assert len(cities) == 1


def test_get_settlements(client: 'Novaposhta'):
    limit = 3
    settlements = client.addresses().get_settlements(limit=limit)
    assert len(settlements) == 3

    second_page = client.addresses().get_settlements(page=2, limit=limit)
    assert len(settlements) == 3
    assert settlements != second_page

    settlements = client.addresses().get_settlements(find_by_string='Киев', limit=limit)
    assert len(settlements) == 2

    settlements = client.addresses().get_settlements(ref=settlements[0].ref)
    assert len(settlements) == 1

    settlements = client.addresses().get_settlements(area_ref=settlements[0].area, limit=limit)
    assert len(settlements) == 3

    settlements = client.addresses().get_settlements(region_ref=settlements[0].region, limit=limit)
    assert len(settlements) == 3

    settlements = client.addresses().get_settlements(warehouse=0)
    assert len(settlements) == 5
    assert all([_.warehouse == 0 for _ in settlements])


def test_warehouse_types(client: 'Novaposhta'):
    warehouse_types = client.addresses().get_warehouse_types()
    assert len(warehouse_types) > 1
    assert type(warehouse_types[0]) == WarehouseType


def test_warehouses(client: 'Novaposhta'):
    limit = 3
    cities = client.addresses().get_cities(limit=10)

    filter = WarehouseFilter(city_name=cities[9].description)

    warehouses = client.addresses().get_warehouses(filter=filter, limit=limit)
    assert len(warehouses) == 1
    assert warehouses[0].city_description == cities[9].description

    filter = WarehouseFilter(language='ru', city_ref=cities[9].ref)

    warehouses = client.addresses().get_warehouses(filter=filter, limit=limit)
    assert len(warehouses) == 1
    assert warehouses[0].city_description == cities[9].description
    assert warehouses[0].city_ref == cities[9].ref

    filter = WarehouseFilter(pos_terminal=1)

    warehouses = client.addresses().get_warehouses(filter=filter, limit=limit)
    assert len(warehouses) == 3
    assert all([warehouse.pos_terminal == 1 for warehouse in warehouses])

    filter = WarehouseFilter(pos_terminal=0)

    warehouses = client.addresses().get_warehouses(filter=filter, limit=limit)
    assert len(warehouses) == 3
    assert all([warehouse.pos_terminal == 0 for warehouse in warehouses])

    # !!!Multiple bool filters not working(1, 1)
    filter = WarehouseFilter(pos_terminal=0, bicycle_parking=1)

    warehouses = client.addresses().get_warehouses(filter=filter, limit=limit)
    assert len(warehouses) == 3
    assert not all([
        warehouse.pos_terminal == 0 and warehouse.bicycle_parking == 1
        for warehouse in warehouses
    ])

    filter = WarehouseFilter(bicycle_parking=1)

    warehouses = client.addresses().get_warehouses(filter=filter, limit=limit)
    assert len(warehouses) == 3
    assert all([warehouse.bicycle_parking == 1 for warehouse in warehouses])

    # Not all warehouse types are filterable. If you filter with the first(zero) type,
    # It's not working
    warehouse_type = client.addresses().get_warehouse_types()[1]
    filter = WarehouseFilter(type_of_warehouse_ref=warehouse_type.ref)

    warehouses = client.addresses().get_warehouses(filter=filter, limit=limit)
    assert len(warehouses) == 3
    assert all([warehouse.type_of_warehouse == warehouse_type.ref for warehouse in warehouses])

    filter = WarehouseFilter(pos_terminal=1)
    warehouses = client.addresses().get_warehouses(filter=filter, limit=limit, page=2)
    assert len(warehouses) == 3
    assert all([warehouse.pos_terminal == 1 for warehouse in warehouses])


def test_get_streets(client: 'Novaposhta'):
    with pytest.raises(InvalidDataError):
        client.addresses().get_city_streets(None)

    cities = client.addresses().get_cities(limit=10)

    streets = client.addresses().get_city_streets(city_ref=cities[0].ref)

    assert len(streets) > 0
    assert all([type(_) == Street for _ in streets])

    substr = streets[0].description[:10]
    streets = client.addresses().get_city_streets(city_ref=cities[0].ref, find_by_string=substr)

    assert len(streets) > 0
    assert all([substr in _.description for _ in streets])

    first_page = client.addresses().get_city_streets(city_ref=cities[0].ref, limit=1)

    assert len(first_page) == 1

    second_page = client.addresses().get_city_streets(city_ref=cities[0].ref, limit=1, page=2)

    assert len(second_page) == 1
    assert second_page != first_page


def test_save(client: 'Novaposhta'):
    counterparty = client.counterparties().list()[0]
    city = client.addresses().get_cities(limit=1)[0]
    street = client.addresses().get_city_streets(city_ref=city.ref, limit=1)[0]

    body = AddressSaveBody(
        street_ref=street.ref, counterparty_ref=counterparty.ref,
        building_number=5, flat=10
    )
    address = client.addresses().save(body=body)
    assert isinstance(address.ref, str)

    same_address = client.addresses().save(body=body)
    assert address.ref == same_address.ref

    body = AddressSaveBody(
        street_ref=street.ref, counterparty_ref=counterparty.ref,
        building_number=10, flat=10
    )
    another_address = client.addresses().save(body=body)
    assert another_address.ref != same_address.ref

    body = AddressSaveBody(
        street_ref=street.ref, counterparty_ref=counterparty.ref,
        building_number=10, flat=10, note='Address note'
    )
    address_with_note = client.addresses().save(body=body)

    assert address_with_note.ref != same_address.ref
    assert address_with_note.ref != another_address.ref

    client.addresses().delete(ref=address.ref)
    client.addresses().delete(ref=another_address.ref)
    client.addresses().delete(ref=address_with_note.ref)


def test_update(client: 'Novaposhta'):
    counterparty = client.counterparties().list()[0]
    city = client.addresses().get_cities(limit=1)[0]
    street = client.addresses().get_city_streets(city_ref=city.ref, limit=1)[0]

    body = AddressSaveBody(
        street_ref=street.ref, counterparty_ref=counterparty.ref,
        building_number=5, flat=10
    )
    new_address = client.addresses().save(body=body)
    assert isinstance(new_address.ref, str)

    body = AddressUpdateBody(
        street_ref=street.ref, counterparty_ref=counterparty.ref,
        building_number=5, flat=10, ref=new_address.ref, note='Comment'
    )
    updated_address = client.addresses().update(body=body)

    assert updated_address.description.endswith('Comment')

    client.addresses().delete(ref=new_address.ref)


def test_delete(client: 'Novaposhta'):
    counterparty = client.counterparties().list()[0]
    city = client.addresses().get_cities(limit=1)[0]
    street = client.addresses().get_city_streets(city_ref=city.ref, limit=1)[0]

    body = AddressSaveBody(
        street_ref=street.ref, counterparty_ref=counterparty.ref,
        building_number=5, flat=10
    )
    new_address = client.addresses().save(body=body)
    deleted = client.addresses().delete(ref=new_address.ref)

    assert deleted.ref == new_address.ref

    body = AddressSaveBody(
        street_ref=street.ref, counterparty_ref=counterparty.ref,
        building_number=5, flat=10
    )
    created_again = client.addresses().save(body=body)
    assert created_again.ref != new_address

    deleted = client.addresses().delete(ref=created_again.ref)

    assert deleted.ref == created_again.ref
