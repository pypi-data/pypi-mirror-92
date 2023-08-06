from .shared import PascalModel


class TimeInterval(PascalModel):
    number: str
    start: str
    end: str
    on_next_day: int


class CommonModel(PascalModel):
    description: str
    ref: str


class CargoType(CommonModel):
    pass


class BackwardDeliveryCargoType(CommonModel):
    pass


class PayerType(PascalModel):
    pass


class Pallet(PascalModel):
    ref: str
    description: str
    description_ru: str
    weight: str


class RedeliveryPayerType(CommonModel):
    pass


class Pack(PascalModel):
    ref: str
    description: str
    description_ru: str
    length: str
    width: str
    height: str
    volumetric_weight: str
    type_of_packing: str


class Wheel(PascalModel):
    ref: str
    description: str
    description_ru: str
    weight: str
    description_type: str


class CargoDescription(CommonModel):
    pass


class MessageCodeText(PascalModel):
    message_code: str
    message_text: str
    message_description_ru: str
    message_description_ua: str


class ServiceType(CommonModel):
    pass


class CounterpartyType(CommonModel):
    pass


class PaymentForm(CommonModel):
    pass


class OwnershipForm(CommonModel):
    full_name: str
