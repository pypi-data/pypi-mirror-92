from typing import Dict, List, Optional, Union

from .shared import PascalModel

__all__ = (
    'CounterpartyAddress',
    'CounterpartyOptions',
    'CounterpartyContactPerson',
    'Counterparty',
    'ContactPerson',
    'NewCounterpartyContactPerson',
    'NewCounterparty',
    'DeleteResponse',
    'ThirdpartyBody',
    'OrganizationBody',
    'SenderBody',
    'UpdateCounterpartyBody',
    'CounterpartyContactPersonUpdateBody',
    'CounterpartyContactPersonSaveBody',
)

from ..const import CounterpartyProperty


class CounterpartyAddress(PascalModel):
    ref: str
    description: str
    city_ref: str
    city_description: str
    street_ref: str
    street_description: str
    building_ref: str
    building_description: str
    note: str
    address_name: str


class CounterpartyOptions(PascalModel):
    filling_warranty: bool
    address_document_delivery: bool
    can_pay_the_third_person: bool
    can_afterpayment_on_goods_cost: bool
    can_non_cash_payment: bool
    can_credit_documents: bool
    can_ew_transporter: bool
    can_signed_documents: bool
    hide_delivery_cost: bool
    block_international_sender_lkk: bool
    international_delivery: bool
    pickup_service: bool
    can_same_day_delivery: bool
    can_same_day_delivery_standart: bool
    can_forwarding_service: bool
    show_delivery_by_hand: bool
    delivery_by_hand: bool
    partial_return: bool
    loyalty_program: bool
    can_sent_from_postomat: bool
    descent_from_floor: bool
    back_delivery_valuable_papers: bool
    backward_delivery_subtypes_documents: bool
    afterpayment_type: str
    credit_documents: bool
    signed_documents: bool
    services: bool
    international_delivery_service_type: bool
    print_marking_allowed_types: Dict[str, bool]
    inventory_order: bool
    debtor: bool
    debtor_params: Union[List[Dict[str, str]], bool]
    calculation_by_factual_weight: bool
    transfer_pricing_conditions: bool
    business_client: bool
    have_money_wallets: bool
    customer_return: bool
    day_customer_return: bool
    main_counterparty: bool
    secure_payment: bool


class CounterpartyContactPerson(PascalModel):
    description: str
    phones: str
    email: str
    ref: str
    last_name: str
    first_name: str
    middle_name: str


class Counterparty(PascalModel):
    description: str
    ref: str
    city: Optional[str] = None
    counterparty: Optional[str] = None
    first_name: str
    last_name: str
    middle_name: str
    ownership_form_ref: Optional[str] = None
    ownership_form_description: str
    edrpou: str
    counterparty_type: str


class ContactPerson(PascalModel):
    ref: str
    description: str
    last_name: str
    first_name: str
    middle_name: Optional[str] = None
    phones: Optional[str] = None
    email: Optional[str] = None


class NewCounterpartyContactPerson(PascalModel):
    success: bool
    data: List[ContactPerson]


class NewCounterparty(PascalModel):
    ref: str
    description: str
    first_name: str
    middle_name: str
    last_name: str
    counterparty: str
    ownership_form: str
    ownership_form_description: str
    edrpou: Union[str, int]
    counterparty_type: str
    contact_person: Optional[NewCounterpartyContactPerson]


class DeleteResponse(PascalModel):
    ref: str


class ThirdpartyBody(PascalModel):
    city_ref: str
    counterparty_type: str = 'Organization'
    counterparty_property: CounterpartyProperty = CounterpartyProperty.THIRDPERSON
    edrpou: Optional[str] = None
    ownership_form: Optional[str] = None


class OrganizationBody(PascalModel):
    counterparty_type: str = 'Organization'
    counterparty_property: CounterpartyProperty = CounterpartyProperty.RECIPIENT
    edrpou: Optional[str] = None


class SenderBody(PascalModel):
    first_name: str
    middle_name: str
    last_name: str
    phone: str
    email: str
    counterparty_type: str = 'PrivatePerson'
    counterparty_property: CounterpartyProperty


class UpdateCounterpartyBody(PascalModel):
    # Private person can only edit phone number
    ref: str
    city_ref: Optional[str] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    edrpou: Optional[str] = None
    ownership_form: Optional[str] = None
    counterparty_type: Optional[str] = None
    counterparty_property: Optional[CounterpartyProperty] = None


class CounterpartyContactPersonSaveBody(PascalModel):
    counterparty_ref: str
    first_name: str
    last_name: str
    middle_name: str
    phone: str


class CounterpartyContactPersonUpdateBody(CounterpartyContactPersonSaveBody):
    ref: str
