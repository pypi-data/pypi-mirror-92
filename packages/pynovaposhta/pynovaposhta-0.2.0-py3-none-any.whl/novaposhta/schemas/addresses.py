from typing import List, Optional, Union
from datetime import datetime

from .shared import PascalModel


__all__ = (
    'SearchAddress',
    'SearchSettlementStreet',
    'SaveAddress',
    'DeleteAddress',
    'Area',
    'City',
    'Settlement',
    'Schedule',
    'Warehouse',
    'WarehouseType',
    'WarehouseFilter',
    'Street',
    'AddressSaveBody',
    'AddressUpdateBody',
)


class SearchAddress(PascalModel):
    present: str
    warehouses: int
    main_description: str
    area: str
    region: str
    settlement_type_code: str
    ref: str
    delivery_city: str
    address_delivery_allowed: bool
    streets_availability: bool
    parent_region_types: str
    parent_region_code: str
    region_types: str
    region_types_code: str


class SearchSettlementStreet(PascalModel):
    settlement_ref: str
    settlement_street_ref: str
    settlement_street_description: str
    present: str
    streets_type: str
    streets_type_description: str
    location: List[float]
    settlement_street_description_ru: str


class SaveAddress(PascalModel):
    ref: str
    description: str


class DeleteAddress(PascalModel):
    ref: str


class Area(PascalModel):
    ref: str
    areas_center: str
    description_ru: str
    description: str


class City(PascalModel):
    description: str
    description_ru: str
    ref: str
    delivery1: str
    delivery2: str
    delivery3: str
    delivery4: str
    delivery5: str
    delivery6: str
    delivery7: str
    area: str
    settlement_type: str
    is_branch: str
    prevent_entry_new_streets_user: Optional[str] = None
    conglomerates: Optional[List[str]] = None
    settlement_type_description_ru: str
    settlement_type_description: str
    special_cash_check: int
    area_description: str
    area_description_ru: str


class Settlement(PascalModel):
    ref: str
    settlement_type: str
    latitude: float
    longitude: float
    description: str
    description_ru: str
    settlement_type_description: str
    settlement_type_description_ru: str
    region: str
    regions_description: str
    regions_description_ru: str
    area: str
    area_description: str
    area_description_ru: str
    index1: int
    index2: int
    delivery1: Optional[Union[int, str]] = None
    delivery2: Optional[Union[int, str]] = None
    delivery3: Optional[Union[int, str]] = None
    delivery4: Optional[Union[int, str]] = None
    delivery5: Optional[Union[int, str]] = None
    delivery6: Optional[Union[int, str]] = None
    delivery7: Optional[Union[int, str]] = None
    special_cash_check: int
    warehouse: int


class Schedule(PascalModel):
    monday: str
    tuesday: str
    wednesday: str
    thursday: str
    friday: str
    saturday: str
    sunday: str


class Warehouse(PascalModel):
    site_key: int
    description: str
    description_ru: str
    short_address: str
    short_address_ru: str
    phone: str
    type_of_warehouse: str
    ref: str
    number: int
    city_ref: str
    city_description: str
    city_description_ru: str
    settlement_ref: str
    settlement_description: str
    settlement_area_description: str
    settlement_regions_description: str
    settlement_type_description: str
    longitude: float
    latitude: float
    post_finance: int
    bicycle_parking: int
    payment_access: int
    pos_terminal: int
    international_shipping: int
    self_service_workplaces_count: int
    total_max_weight_allowed: int
    place_max_weight_allowed: int
    reception: Schedule
    delivery: Schedule
    schedule: Schedule
    district_code: str
    warehouse_status: str
    warehouse_status_date: datetime
    category_of_warehouse: str
    direct: str
    region_city: str


class WarehouseType(PascalModel):
    ref: str
    description: str
    description_ru: str


class WarehouseFilter(PascalModel):
    """
    Warehouse list filter

    Attributes:
        :var bicycle_parking: Whether warehouse has bicycle parking. 1 or 0.
        :var type_of_warehouse_ref: Warehouse ref type, from `WarehouseType.ref`
        :var post_finance: Whether warehouse has post-finance terminal. 1 or 0.
        :var city_name: Name of the settlement. Can be partial.
        :var city_ref: Ref of the settlement.
        :var pos_terminal: Whether warehouse has bicycle parking. 1 or 0.
        :var language: Language of the warehouse description to return. Default is uk. Can be ru or uk.
    """

    bicycle_parking: Optional[int] = None
    type_of_warehouse_ref: Optional[str] = None
    post_finance: Optional[int] = None
    city_name: Optional[str] = None
    city_ref: Optional[str] = None
    pos_terminal: Optional[int] = None
    language: Optional[str] = None


class Street(PascalModel):
    description: str
    ref: str
    streets_type_ref: str
    streets_type: str


class AddressSaveBody(PascalModel):
    counterparty_ref: str
    street_ref: str
    building_number: int
    flat: int
    note: Optional[str] = None


class AddressUpdateBody(AddressSaveBody):
    ref: str
