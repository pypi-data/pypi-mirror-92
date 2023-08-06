from typing import Optional
from datetime import datetime

from .shared import PascalModel


class RedirectPossibility(PascalModel):
    ref: str
    number: str
    payer_type: str
    payment_method: str
    service_type: str
    warehouse_ref: str
    warehouse_description: str
    city_recipient: str
    city_recipient_description: str
    settlement_recipient: str
    settlement_recipient_description: str
    settlement_type: str
    counterparty_recipient_ref: str
    counterparty_recipient_description: str
    recipient_name: str
    phone_sender: str
    phone_recipient: str
    document_weight: str


class RedirectAddressBody(PascalModel):
    order_type: str
    int_doc_number: str
    customer: str
    service_type: str

    recipient_warehouse: Optional[str] = None
    recipient_settlement: Optional[str] = None
    recipient_settlement_street: Optional[str] = None
    building_number: Optional[str] = None
    note_address_recipient: Optional[str] = None

    recipient: str
    recipient_contact_name: str
    recipient_phone: str
    payer_type: str
    payment_method: str
    note: str


class RedirectAddress(PascalModel):
    number: str
    ref: str


class SaveResponse(PascalModel):
    number: str
    ref: str


class DeleteResponse(PascalModel):
    number: str


class Order(PascalModel):
    order_ref: str
    order_number: str
    date_time: str
    order_status: str
    document_number: str
    note: str
    city_recipient: str
    recipient_address: str
    counterparty_recipient: str
    recipient_name: str
    phone_recipient: str
    payer_type: str
    payment_method: str
    delivery_cost: str
    estimated_delivery_date: str
    express_waybill_number: str
    express_waybill_status: str


class EWOrder(PascalModel):
    order_ref: str
    order_number: str
    order_type: str
    document_number: str
    date_time: datetime
    order_status: str
    cost: int
    before_change_sender_phone: str
    after_change_sender_phone: str


class CheckPossibilityChangeEW(PascalModel):
    can_change_sender: bool
    can_change_recipient: bool
    can_change_payer_type_or_payment_method: bool
    sender_phone: str
    contact_person_sender: str
    recipient_phone: str
    contact_person_recipient: str
    payer_type: str
    payment_method: str
    sender_counterparty: str
    recipient_counterparty: str


class AdditionalServiceBody(PascalModel):
    int_doc_number: str
    order_type: str
    sender_contact_name: str
    sender_phone: str
    recipient: str
    recipient_contact_name: str
    recipient_phone: str
    payer_type: str
    payment_method: str


class ReturnPossibility(PascalModel):
    non_cash: bool
    city: str
    counterparty: str
    contact_person: str
    address: str
    phone: str
    ref: str


class ReturnReason(PascalModel):
    ref: str
    description: str


class ReturnReasonSubtype(PascalModel):
    ref: str
    description: str
    reason_ref: str


class ReturnOrder(PascalModel):
    order_ref: str
    order_number: str
    order_status: str
    document_number: str
    counterparty_recipient: str
    contact_person_recipient: str
    address_recipient: str
    delivery_cost: str
    estimated_delivery_date: str
    express_waybill_number: str
    express_waybill_status: str


class ReturnOrderBody(PascalModel):
    int_doc_number: str
    payment_method: str
    reason: str
    subtype_reason: str
    note: Optional[str] = None
    order_type: str
    return_address_ref: str
