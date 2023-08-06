from typing import Optional

from .abstract import AbstractNovaposhta
from .models import (
    addresses, common, counterparties as conterparties_model, internet_documents, scan_sheets
)


class Novaposhta(AbstractNovaposhta):
    def addresses(self, base_url: Optional[str] = None) -> addresses.Address:
        return addresses.Address(client=self, base_url=base_url)

    def common(self, base_url: Optional[str] = None) -> common.Common:
        return common.Common(client=self, base_url=base_url)

    def counterparties(self, base_url: Optional[str] = None) -> conterparties_model.Counterparty:
        return conterparties_model.Counterparty(client=self, base_url=base_url)

    def contact_persons(self, base_url: Optional[str] = None) -> conterparties_model.ContactPerson:
        return conterparties_model.ContactPerson(client=self, base_url=base_url)

    def internet_documents(self, base_url: Optional[str] = None) -> internet_documents.InternetDocument:
        return internet_documents.InternetDocument(
            client=self, base_url=base_url
        )

    @property
    def scan_sheets(self) -> scan_sheets.ScanSheet:
        return scan_sheets.ScanSheet(self)
