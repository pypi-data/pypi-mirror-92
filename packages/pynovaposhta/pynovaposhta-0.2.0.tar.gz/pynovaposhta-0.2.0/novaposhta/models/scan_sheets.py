from typing import List, Optional
from datetime import date

import httpx

from .abstract import AbstractClient
from ..schemas.scan_sheets import (
    Document, ScanSheetListItem, ScanSheet as ScanSheetSchema, ScanSheetDeleted
)


class ScanSheet(AbstractClient):
    def insert(self, documents: List[str], ref: Optional[str] = None, dt: date = None):
        request = self.build_request(
            url=self.build_url('insertDocuments'),
            json=self.build_params(
                'insertDocuments',
                {'DocumentRefs': documents, 'Ref': ref, 'Date': dt}
            ),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=Document)

    def get(self, ref: str, counterparty_ref: str):
        request = self.build_request(
            url=self.build_url('getScanSheet'),
            json=self.build_params(
                'getScanSheet',
                {'CounterpartyRef': counterparty_ref, 'Ref': ref}
            ),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=ScanSheetSchema)

    def list(self):
        request = self.build_request(
            url=self.build_url('getScanSheetList'),
            json=self.build_params(
                'getScanSheetList',
                {}
            ),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=ScanSheetListItem)

    def delete(self, refs: List[str]):
        request = self.build_request(
            url=self.build_url('deleteScanSheet'),
            json=self.build_params(
                'deleteScanSheet',
                {
                    'ScanSheetRefs': refs
                }
            ),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=ScanSheetDeleted)

    def remove_documents(self, refs: List[str], ref: str):
        request = self.build_request(
            url=self.build_url('removeDocuments'),
            json=self.build_params(
                'removeDocuments',
                {
                    'DocumentRefs': refs,
                    'Ref': ref
                }
            ),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=ScanSheetDeleted)
