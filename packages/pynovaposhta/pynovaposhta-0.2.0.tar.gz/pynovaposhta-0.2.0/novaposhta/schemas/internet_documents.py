from datetime import datetime, date
from typing import Optional, List, Union

from .shared import PascalModel, CamelModel


class DocumentGeoData(PascalModel):
    recipient_address_name: str
    recipient_area: str
    recipient_area_regions: str
    recipient_city_name: str
    recipient_flat: str
    recipient_house: str


class DocumentSettlementAddressData(PascalModel):
    sender_warehouse_ref: str
    recipient_warehouse_ref: str
    sender_warehouse_number: str
    recipient_warehouse_number: str
    sender_settlement_ref: str
    recipient_settlement_ref: str
    sender_settlement_description: str
    recipient_settlement_description: str
    sender_settlement_street_description: str
    recipient_settlement_street_description: str
    sender_settlement_street_ref: str
    recipient_settlement_street_ref: str
    sender_house_number: str
    recipient_house_number: str
    sender_flat_number: str
    recipient_flat_number: str
    sender_address_note: str
    recipient_address_note: str


class Document(PascalModel):
    ref: str
    deletion_mark: str
    date_time: str
    preferred_delivery_date: str
    weight: int
    seats_amount: int
    int_doc_number: int
    cost: int
    service_type: str
    description: str
    city_sender: str
    city_recipient: str
    state: str
    sender_address: str
    recipient_address: str
    sender: str
    contact_sender: str
    recipient: str
    contact_recipient: str
    cost_on_site: int
    payer_type: str
    payment_method: str
    afterpayment_on_goods_cost: str
    cargo_type: str
    packing_number: str
    additional_information: str
    senders_phone: str
    recipients_phone: str
    loyalty_card: str
    posted: str
    route: str
    ew_number: str
    saturday_delivery: str
    express_waybill: str
    car_call: str
    delivery_date_from: str
    vip: str
    last_modification_date: str
    receipt_date: str
    redelivery: str
    saturday_delivery_string: str
    note: str
    third_person: str
    forwarding: str
    number_of_floors_lifting: str
    statement_of_acceptance_transfer_cargo_id: str
    settlement_sender: str
    settlement_recipient: str
    warehouse_sender: str
    warehouse_recipient: str
    state_id: str
    state_name: str
    recipient_full_name: str
    recipient_post: str
    recipient_date_time: str
    rejection_reason: str
    online_credit_status: str
    city_sender_description: str
    city_recipient_description: str
    sender_description: str
    recipient_description: str
    recipient_contact_phone: str
    recipient_contact_person: str
    sender_contact_person: str
    sender_address_description: str
    recipient_address_description: str
    printed: str
    changed_data_ew: str
    ew_date_created: str
    scheduled_delivery_date: str
    estimated_delivery_date: str
    region_code: str
    date_last_updated_status: str
    date_last_print: str
    create_time: str
    scan_sheet_number: str
    scan_sheet_printed: str
    info_reg_client_barcodes: str
    state_pay_id: str
    state_pay_name: str
    backward_delivery_cargo_type: str
    backward_delivery_sum: str
    backward_delivery_money: str
    backward_delivery_data_documents: str
    sender_counterparty_type: str
    elevator_recipient: str
    recipient_counterparty_type: str
    delivery_by_hand: str
    forwarding_count: str
    original_geo_data: DocumentGeoData
    ownership_form: str
    edrpou: str
    red_box_barcode: str
    recipient_city_ref: str
    recipient_street_ref: str
    recipient_warehouse_ref: str
    is_take_attorney: str
    same_day_delivery: str
    time_interval: str
    time_interval_ref: str
    time_interval_string: str
    express_pallet: str
    term_extension: str
    term_extension_days: str
    avia_delivery: str
    system: str
    secure_payment: str
    promocode: str
    special_cargo: str
    settlment_address_data: DocumentSettlementAddressData


class DeliveryDate(PascalModel):
    date: datetime
    timezone_type: str
    timezone: str


class DeliveryPrice(PascalModel):
    cost_redelivery: int
    assessed_cost: int
    cost: int
    cost_pack: int


class UpdateDocumentResult(PascalModel):
    ref: str
    cost_on_site: int
    estimated_delivery_date: date
    int_doc_number: str
    type_document: str


class SaveDocumentAddressBody(PascalModel):
    new_address: bool
    payer_type: str
    payment_method: str
    cargo_type: str
    volume_general: Optional[int] = None
    weight: int
    service_type: str
    seats_amount: str
    description: str
    cost: int
    city_sender: str
    sender: str
    sender_address: str
    contact_sender: str
    senders_phone: int
    recipient_city_name: str
    recipient_area: str
    recipient_area_regions: str
    recipient_address_name: str
    recipient_house: str
    recipient_flat: str
    recipient_name: str
    recipient_type: str
    recipients_phone: str
    date_time: str
    settlement_type: Optional[str] = None
    recipient_name: Optional[str] = None
    recipient_type: Optional[str] = None
    ownership_form: Optional[str] = None
    recipient_contact_name: Optional[str] = None
    EDRPOU: Optional[str] = None


class SaveDocumentBody(PascalModel):
    payer_type: str
    payment_method: str
    date_time: str
    cargo_type: str
    volume_general: Optional[int] = None
    weight: int
    service_type: str
    seats_amount: str
    description: str
    cost: int
    city_sender: str
    sender: str
    sender_address: str
    contact_sender: str
    senders_phone: int
    city_recipient: str
    recipient: str
    recipient_address: str
    contact_recipient: str
    recipients_phone: int
    red_box_barcode: Optional[str] = None


class ParcelOptionsSeat(CamelModel):
    volumetric_volume: Optional[str] = None
    volumetric_width: Optional[str] = None
    volumetric_length: Optional[str] = None
    volumetric_height: Optional[str] = None
    weight: Optional[str] = None


class SaveDocumentParcelBody(PascalModel):
    sender: str
    cash: Optional[str] = None
    date_time: str
    cargo_type: str
    options_seat: List[ParcelOptionsSeat]
    service_type: str
    seats_amount: str
    description: str
    cost: int
    city_sender: Optional[str] = None
    sender: Optional[str] = None
    sender_address: str
    contact_sender: str
    senders_phone: int
    city_recipient: str
    recipient: str
    recipient_address: Optional[str] = None
    contact_recipient: str
    recipients_phone: int


class BackwardDeliveryDocumentMultipleTypesService(PascalModel):
    attorney: bool
    waybill_new_post_with_stamp: bool
    user_actions: str


class BackwardDeliveryDocumentMultipleTypes(PascalModel):
    payer_type: str
    cargo_type: str
    services: BackwardDeliveryDocumentMultipleTypesService


class BackwardDeliveryMoney(PascalModel):
    payer_type: str
    cargo_type: str = 'CreditDocuments'
    redelivery_string: str


class BackwardDeliveryCreditDocument(PascalModel):
    payer_type: str
    cargo_type: str = 'SignedDocuments'
    redelivery_string: str


class BackwardDeliverySign(PascalModel):
    payer_type: str
    cargo_type: str
    redelivery_string: str


class BackwardDeliveryTwoTypesTray(PascalModel):
    cargo_description: str
    amount: str


class BackwardDeliveryTwoTypes(PascalModel):
    payer_type: str
    cargo_type: str
    redelivery_string: str
    trays: List[BackwardDeliveryTwoTypesTray]


class BackwardDeliveryDocument(PascalModel):
    payer_type: str
    cargo_type: str
    redelivery_string: str


class BackwardDeliveryOther(PascalModel):
    payer_type: str
    cargo_type: str
    redelivery_string: str


class SaveDocumentBackwardDeliveryBody(PascalModel):
    payer_type: str
    payment_method: str
    date_time: str
    cargo_type: str
    volume_general: str
    weight: str
    service_type: str
    seats_amount: str
    description: str
    cost: str
    city_sender: str
    sender: str
    sender_address: str
    contact_sender: str
    senders_phone: str
    city_recipient: str
    recipient: str
    recipient_address: str
    contact_recipient: str
    recipients_phone: str
    backward_delivery_data: List[Union[
        BackwardDeliveryDocumentMultipleTypesService,
        BackwardDeliveryDocumentMultipleTypes,
        BackwardDeliveryMoney,
        BackwardDeliveryCreditDocument,
        BackwardDeliverySign,
        BackwardDeliveryTwoTypes,
        BackwardDeliveryDocument,
        BackwardDeliveryOther,
    ]]


class SaveDocumentResult(PascalModel):
    ref: str
    cost_on_site: int
    estimated_delivery_date: date
    int_doc_number: str
    type_document: str
    region_code: Optional[str] = None
    region_city: Optional[str] = None


class TrackingStatusDocumentBody(PascalModel):
    document_number: str
    phone: str


class TrackingStatusDocument(PascalModel):
    number: str
    redelivery: int
    redelivery_sum: int
    redelivery_num: str
    redelivery_payer: str
    owner_document_type: str
    last_created_on_the_basis_document_type: str
    last_created_on_the_basis_payer_type: str
    last_created_on_the_basis_date_time: str
    last_transaction_status_g_m: str
    last_transaction_date_time_g_m: str
    date_created: datetime
    document_weight: float
    check_weight: int
    document_cost: int
    sum_before_check_weight: int
    payer_type: str
    recipient_full_name: str
    recipient_date_time: datetime
    scheduled_delivery_date: date
    payment_method: str
    cargo_description_string: str
    cargo_type: str
    city_sender: str
    city_recipient: str
    warehouse_recipient: str
    counterparty_type: str
    afterpayment_on_goods_cost: int
    service_type: str
    undelivery_reasons_subtype_description: str
    warehouse_recipient_number: int
    last_created_on_the_basis_number: str
    phone_recipient: str
    recipient_full_name_ew: str
    warehouse_recipient_internet_address_ref: str
    marketplace_partner_token: str
    client_barcode: str
    recipient_address: str
    counterparty_recipient_description: str
    counterparty_sender_type: str
    date_scan: datetime
    payment_status: str
    payment_status_date: str
    amount_to_pay: str
    amount_paid: str
    status: str
    status_code: str
    ref_ew: str
    backward_delivery_sub_types_services: str
    backward_delivery_sub_types_actions: str
    undelivery_reasons: str


class DeletedRef(PascalModel):
    ref: str


class GeneratedReport(PascalModel):
    ref: str
    date_time: datetime
    preferred_delivery_date: datetime
    weight: str
    seats_amount: str
    int_doc_number: str
    cost: str
    city_sender: str
    city_recipient: str
    state: str
    sender_address: str
    recipient_address: str
    cost_on_site: str
    payer_type: str
    payment_method: str
    afterpayment_on_goods_cost: str
    packing_number: str
    number: str
    posted: str
    deletion_mark: str
    cargo_type: str
    route: str
    ew_number: str
    description: str
    saturday_delivery: str
    express_waybill: str
    car_call: str
    service_type: str
    delivery_date_from: str
    vip: str
    additional_information: str
    last_modification_date: str
    receipt_date: str
    loyalty_card: str
    sender: str
    contact_sender: str
    senders_phone: str
    recipient: str
    contact_recipient: str
    recipients_phone: str
    redelivery: str
    saturday_delivery_string: str
    note: str
    third_person: str
    forwarding: str
    number_of_floors_lifting: str
    statement_of_acceptance_transfer_cargo_id: str
    state_id: int
    state_name: str
    recipient_full_name: str
    recipient_post: str
    recipient_date_time: str
    rejection_reason: str
    city_sender_description: str
    city_recipient_description: str
    sender_description: str
    recipient_description: str
    recipient_contact_phone: str
    recipient_contact_person: str
    sender_address_description: str
    recipient_address_description: str
    printed: str
    fulfillment: int
    estimated_delivery_date: datetime
    date_last_updated_status: datetime
    create_time: datetime
    scan_sheet_number: str
    info_reg_client_barcodes: str
    state_pay_id: str
    state_pay_name: str
    backward_delivery_cargo_type: str


class SaveAddServiceBody(PascalModel):
    # Additional services
    is_take_attorney: Optional[str] = None
    saturday_delivery: Optional[str] = None
    afterpayment_on_goods_cost: Optional[str] = None
    local_express: Optional[str] = None
    time_interval: Optional[str] = None
    preferred_delivery_date: Optional[str] = None
    packing_number: Optional[str] = None
    info_reg_client_barcodes: Optional[str] = None
    accompanying_documents: Optional[str] = None
    additional_information: Optional[str] = None
    number_of_floors_lifting: Optional[str] = None
    elevator: Optional[str] = None
    delivery_by_hand: Optional[str] = None
    delivery_by_hand_recipients: Optional[List[str]] = None
    forwarding_count: Optional[List[str]] = None
    red_box_barcode: Optional[List[str]] = None
    avia_delivery: Optional[List[str]] = None
    special_cargo: Optional[List[str]] = None

    # Document data
    payer_type: str
    payment_method: str
    date_time: str
    cargo_type: str
    volume_general: str
    weight: str
    service_type: str
    seats_amount: str
    description: str
    cost: str
    city_sender: str
    sender: str
    sender_address: str
    contact_sender: str
    senders_phone: str
    city_recipient: str
    recipient: str
    recipient_address: str
    contact_recipient: str
    recipients_phone: str


class CargoDetail(PascalModel):
    cargo_description: str
    amount: str


class SaveTypeCargoBody(PascalModel):
    # Additional services
    # one of: TiresWheels, Pallet, Documents
    cargo_type: str
    cargo_details: Optional[List[CargoDetail]] = None
    options_seat: Optional[List[ParcelOptionsSeat]] = None

    # Document data
    payer_type: str
    payment_method: str
    date_time: str
    cargo_type: str
    volume_general: str
    weight: str
    service_type: str
    seats_amount: str
    description: str
    cost: str
    city_sender: str
    sender: str
    sender_address: str
    contact_sender: str
    senders_phone: str
    city_recipient: str
    recipient: str
    recipient_address: str
    contact_recipient: str
    recipients_phone: str
