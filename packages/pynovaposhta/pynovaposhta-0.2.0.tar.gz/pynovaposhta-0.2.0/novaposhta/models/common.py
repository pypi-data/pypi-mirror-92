from datetime import date
from typing import Optional

import httpx

from .abstract import AbstractClient
from ..schemas.common import TimeInterval, CargoType, BackwardDeliveryCargoType, Pallet, PayerType, RedeliveryPayerType, \
    Pack, Wheel, CargoDescription, MessageCodeText, ServiceType, CounterpartyType, PaymentForm, OwnershipForm


class Common(AbstractClient):
    MODEL = 'Common'

    def get_time_intervals(self, recipient_city_ref: str, date_time: date):
        request = self.build_request(
            url=self.build_url('getTimeIntervals'),
            json=self.build_params(
                'getTimeIntervals',
                {"RecipientCityRef": recipient_city_ref, "DateTime": date_time}
            ),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=TimeInterval)

    def get_cargo_types(self):
        request = self.build_request(
            url=self.build_url('getCargoType'),
            json=self.build_params('getCargoType'),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=CargoType)

    def get_backward_delivery_cargo_type(self):
        request = self.build_request(
            url=self.build_url('getBackwardDeliveryCargoTypes'),
            json=self.build_params('getBackwardDeliveryCargoTypes'),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=BackwardDeliveryCargoType)

    def get_pallets(self):
        request = self.build_request(
            url=self.build_url('getPalletsList'),
            json=self.build_params('getPalletsList'),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=Pallet)

    def get_payer_types(self):
        request = self.build_request(
            url=self.build_url('getTypesOfPayers'),
            json=self.build_params('getTypesOfPayers'),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=PayerType)

    def get_redelivery_payer_types(self):
        request = self.build_request(
            url=self.build_url('getTypesOfPayersForRedelivery'),
            json=self.build_params('getTypesOfPayersForRedelivery'),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=RedeliveryPayerType)

    def get_packs(self):
        request = self.build_request(
            url=self.build_url('getPackList'),
            json=self.build_params('getPackList'),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=Pack)

    def get_tires_wheels(self):
        request = self.build_request(
            url=self.build_url('getTiresWheelsList'),
            json=self.build_params('getTiresWheelsList'),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=Wheel)

    def get_cargo_description(self, find_by_string: Optional[str] = None, page: int = 1):
        request = self.build_request(
            url=self.build_url('getCargoDescriptionList'),
            json=self.build_params('getCargoDescriptionList', {
                'FindByString': find_by_string,
                'Page': page

            }),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=CargoDescription)

    def get_message_code_text(self):
        request = self.build_request(
            url=self.build_url('getMessageCodeText'),
            json=self.build_params('getMessageCodeText', {

            }),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=MessageCodeText)

    def get_service_types(self):
        request = self.build_request(
            url=self.build_url('getServiceTypes'),
            json=self.build_params('getServiceTypes', {

            }),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=ServiceType)

    def get_counterparty_types(self):
        request = self.build_request(
            url=self.build_url('getTypesOfCounterparties'),
            json=self.build_params('getTypesOfCounterparties', {

            }),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=CounterpartyType)

    def get_payment_forms(self):
        request = self.build_request(
            url=self.build_url('getPaymentForms'),
            json=self.build_params('getPaymentForms', {

            }),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=PaymentForm)

    def get_ownership_forms(self):
        request = self.build_request(
            url=self.build_url('getOwnershipFormsList'),
            json=self.build_params('getOwnershipFormsList', {

            }),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=OwnershipForm)
