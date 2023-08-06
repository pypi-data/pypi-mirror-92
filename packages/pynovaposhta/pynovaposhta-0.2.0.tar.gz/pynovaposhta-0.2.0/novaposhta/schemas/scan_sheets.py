from datetime import datetime

from .shared import PascalModel


class Document(PascalModel):
    ref: str
    number: int
    date: str


class ScanSheet(PascalModel):
    ref: str
    number: str
    date_time: datetime
    count: str
    city_sender_ref: str
    city_sender: str
    sender_address_ref: str
    sender_address: str
    sender_ref: str
    sender: str


class ScanSheetListItem(PascalModel):
    ref: str
    number: str
    date_time: datetime
    printed: str


class ScanSheetDeleted(PascalModel):
    ref: str
    number: str
