from datetime import date
from typing import Optional

import httpx

from .abstract import AbstractClient
from ..schemas.additional_service_general import RedirectPossibility, RedirectAddressBody, DeleteResponse, Order, \
    EWOrder, CheckPossibilityChangeEW, AdditionalServiceBody, SaveResponse, ReturnPossibility, ReturnReason, \
    ReturnReasonSubtype, ReturnOrder, ReturnOrderBody


class InternetDocument(AbstractClient):
    MODEL = 'AdditionalServiceGeneral'

    def check_possibility_for_redirecting(self, number: int):
        request = self.build_request(
            url=self.build_url('checkPossibilityForRedirecting'),
            json=self.build_params(
                'checkPossibilityForRedirecting',
                {'Number': number}
            ),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=RedirectPossibility)

    def save(self, body: RedirectAddressBody):
        request = self.build_request(
            url=self.build_url('save'),
            json=self.build_params(
                'save',
                body.dict()
            ),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=RedirectPossibility)

    def delete(self, ref: str, order_type: str):
        request = self.build_request(
            url=self.build_url('delete'),
            json=self.build_params(
                'delete',
                {
                    "Ref": ref,
                    "OrderType": order_type
                }
            ),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=DeleteResponse)


class AdditionalService(AbstractClient):
    MODEL = 'AdditionalService'

    def get_redirection_orders_list(
        self, number: str, ref: str, begin_date: date, end_date: date,
        page: int = 1, limit: int = 100
    ):
        request = self.build_request(
            url=self.build_url('getRedirectionOrdersList'),
            json=self.build_params(
                'getRedirectionOrdersList',
                {
                    "Number": number,
                    "Ref": ref,
                    "BeginDate": begin_date,
                    "EndDate": end_date,
                    "Page": page,
                    "Limit": limit
                }
            ),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=Order)

    def get_change_ew_orders_list(
        self, number: str, ref: str, begin_date: date, end_date: date,
        page: int = 1, limit: int = 100
    ):
        request = self.build_request(
            url=self.build_url('getChangeEWOrdersList'),
            json=self.build_params(
                'getChangeEWOrdersList',
                {
                    "Number": number,
                    "Ref": ref,
                    "BeginDate": begin_date,
                    "EndDate": end_date,
                    "Page": page,
                    "Limit": limit
                }
            ),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=EWOrder)

    def delete(self, ref: str):
        request = self.build_request(
            url=self.build_url('delete'),
            json=self.build_params(
                'delete',
                {
                    "Ref": ref,
                }
            ),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=DeleteResponse)

    def check_possibility_change_ew(self, doc_number: int):
        request = self.build_request(
            url=self.build_url('CheckPossibilityChangeEW'),
            json=self.build_params(
                'CheckPossibilityChangeEW',
                {
                    "IntDocNumber": doc_number,
                }
            ),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=CheckPossibilityChangeEW)

    def save(self, body: AdditionalServiceBody):
        request = self.build_request(
            url=self.build_url('save'),
            json=self.build_params(
                'save',
                body.dict()
            ),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=SaveResponse)

    def check_possibility_create_return(self, number: str):
        request = self.build_request(
            url=self.build_url('CheckPossibilityCreateReturn'),
            json=self.build_params(
                'CheckPossibilityCreateReturn',
                {'Number': number}
            ),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=ReturnPossibility)

    def get_return_reasons(self):
        request = self.build_request(
            url=self.build_url('getReturnReasons'),
            json=self.build_params(
                'getReturnReasons',
                {}
            ),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=ReturnReason)

    def get_return_reason_subtype(self, reason: str):
        request = self.build_request(
            url=self.build_url('getReturnReasons'),
            json=self.build_params(
                'getReturnReasons',
                {"ReasonRef": reason}
            ),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=ReturnReasonSubtype)

    def get_return_orders(
        self,
        number: Optional[str] = None,
        ref: Optional[str] = None,
        begin_date: Optional[date] = None,
        end_date: Optional[date] = None,
        page: Optional[int] = 1,
        limit: Optional[int] = 100,
    ):
        request = self.build_request(
            url=self.build_url('getReturnOrdersList'),
            json=self.build_params(
                'getReturnOrdersList',
                {
                    "Number": number,
                    "Ref": ref,
                    "BeginDate": begin_date,
                    "EndDate": end_date,
                    "Page": page,
                    "Limit": limit,
                }
            ),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=ReturnOrder)

    def delete_return_order(self, ref: str):
        request = self.build_request(
            url=self.build_url('delete'),
            json=self.build_params(
                'delete',
                {"Ref": ref}
            ),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=DeleteResponse)

    def create_return_order(self, body: ReturnOrderBody):
        request = self.build_request(
            url=self.build_url('save'),
            json=self.build_params(
                'save',
                body.dict()
            ),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=SaveResponse)
