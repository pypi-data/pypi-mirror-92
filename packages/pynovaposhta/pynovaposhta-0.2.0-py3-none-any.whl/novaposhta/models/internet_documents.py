from datetime import date
from typing import Optional, List

import httpx

from .abstract import AbstractClient
from ..schemas.internet_documents import Document, DeliveryDate, DeliveryPrice, UpdateDocumentResult, SaveDocumentBody, \
    SaveDocumentResult, SaveDocumentAddressBody, SaveDocumentParcelBody, TrackingStatusDocumentBody, DeletedRef, \
    TrackingStatusDocument, GeneratedReport, SaveAddServiceBody, SaveDocumentBackwardDeliveryBody, SaveTypeCargoBody


class InternetDocument(AbstractClient):
    MODEL = 'InternetDocument'

    def list(
        self,
        date_time_from: date,
        date_time_to: date,
        page: str,
        get_full_list: str,
        date_time: date
    ):
        request = self.build_request(
            url=self.build_url('getDocumentList'),
            json=self.build_params(
                'getDocumentList',
                {
                    "DateTimeFrom": date_time_from,
                    "DateTimeTo": date_time_to,
                    "Page": page,
                    "GetFullList": get_full_list,
                    "DateTime": date_time,
                }
            ),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=Document)

    def get_delivery_date(
        self,
        service_type: str,
        city_sender: str,
        city_recipient: str,
        date_time: Optional[date] = None,
    ):

        request = self.build_request(
            url=self.build_url('getDocumentList'),
            json=self.build_params(
                'getDocumentList',
                {
                     "DateTime": date_time,
                     "ServiceType": service_type,
                     "CitySender": city_sender,
                     "CityRecipient": city_recipient
                }
            ),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=DeliveryDate)

    def get_delivery_price(
        self,
        city_sender: str,
        city_recipient: str,
        weight: str,
        service_type: str,
        cost: str,
        cargo_type: str,
        seats_amount: str,
        pack_calculate: str,
        redelivery_calculate: str,
    ):
        request = self.build_request(
            url=self.build_url('getDocumentPrice'),
            json=self.build_params(
                'getDocumentPrice',
                {
                    "CitySender": city_sender,
                    "CityRecipient": city_recipient,
                    "Weight": weight,
                    "ServiceType": service_type,
                    "Cost": cost,
                    "CargoType": cargo_type,
                    "SeatsAmount": seats_amount,
                    "PackCalculate": pack_calculate,
                    "RedeliveryCalculate": redelivery_calculate
                }
            ),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=DeliveryPrice)

    def update(
        self,
        ref: str,
        payer_type: str,
        payment_method: str,
        date_time: str,
        cargo_type: str,
        volume_general: int,
        weight: int,
        service_type: str,
        seats_amount: str,
        description: str,
        cost: int,
        city_sender: str,
        sender: str,
        sender_address: str,
        contact_sender: str,
        senders_phone: int,
        city_recipient: str,
        recipient: str,
        recipient_address: str,
        contact_recipient: str,
        recipients_phone: int,
    ):
        request = self.build_request(
            url=self.build_url('update'),
            json=self.build_params(
                'update',
                {
                    "Ref": ref,
                    "PayerType": payer_type,
                    "PaymentMethod": payment_method,
                    "DateTime": date_time,
                    "CargoType": cargo_type,
                    "VolumeGeneral": volume_general,
                    "Weight": weight,
                    "ServiceType": service_type,
                    "SeatsAmount": seats_amount,
                    "Description": description,
                    "Cost": cost,
                    "CitySender": city_sender,
                    "Sender": sender,
                    "SenderAddress": sender_address,
                    "ContactSender": contact_sender,
                    "SendersPhone": senders_phone,
                    "CityRecipient": city_recipient,
                    "Recipient": recipient,
                    "RecipientAddress": recipient_address,
                    "ContactRecipient": contact_recipient,
                    "RecipientsPhone": recipients_phone,
                }
            ),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=UpdateDocumentResult)

    def save(self, body: SaveDocumentBody):
        request = self.build_request(
            url=self.build_url('save'),
            json=self.build_params(
                'save',
                body.dict()
            ),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=SaveDocumentResult)

    def save_address(self, body: SaveDocumentBody):
        request = self.build_request(
            url=self.build_url('save_address'),
            json=self.build_params(
                'save',
                body.dict()
            ),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=SaveDocumentResult)

    def save_warehouse(self, body: SaveDocumentAddressBody):
        request = self.build_request(
            url=self.build_url('save_warehouse'),
            json=self.build_params(
                'save',
                body.dict()
            ),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=SaveDocumentResult)

    def save_postomat(self, body: SaveDocumentParcelBody):
        request = self.build_request(
            url=self.build_url('save_postomat'),
            json=self.build_params(
                'save',
                body.dict()
            ),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=SaveDocumentResult)

    def save_redelivery(self, body: SaveDocumentBackwardDeliveryBody):
        request = self.build_request(
            url=self.build_url('save_redelivery'),
            json=self.build_params(
                'save',
                body.dict()
            ),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=SaveDocumentResult)

    def delete(self, ref: str):
        request = self.build_request(
            url=self.build_url('delete'),
            json=self.build_params(
                'delete',
                {
                    'DocumentRefs': ref
                }
            ),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=DeletedRef)

    def generate_report(self, dt: date, refs: List[str], type: str):
        request = self.build_request(
            url=self.build_url('generateReport'),
            json=self.build_params(
                'generateReport',
                {
                    'DateTime': dt,
                    'DocumentRefs': refs,
                    'Type': type
                }
            ),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=GeneratedReport)

    def save_add_services(self, body: SaveAddServiceBody):
        request = self.build_request(
            url=self.build_url('save_add_services'),
            json=self.build_params(
                'save',
                body.dict()
            ),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=SaveDocumentResult)

    def save_type_cargo(self, body: SaveTypeCargoBody):
        request = self.build_request(
            url=self.build_url('save_type_cargo'),
            json=self.build_params(
                'save',
                body.dict()
            ),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=SaveDocumentResult)


class Tracking(AbstractClient):
    MODEL = 'TrackingDocument'

    def get_status_documents(self, documents: List[TrackingStatusDocumentBody]):
        request = self.build_request(
            url=self.build_url('getStatusDocuments'),
            json=self.build_params(
                'getStatusDocuments',
                {
                    'Documents': [_.dict() for _ in documents]
                }
            ),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=TrackingStatusDocument)
