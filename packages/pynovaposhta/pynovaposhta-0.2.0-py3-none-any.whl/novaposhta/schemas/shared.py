from humps import pascalize, camelize
from pydantic import BaseModel

MANUAL_FIELD_NAMES = {
    'pos_terminal': 'POSTerminal',
    'on_next_day': 'onNextDay',
    'message_description_ru': 'MessageDescriptionRU',
    'message_description_ua': 'MessageDescriptionUA',
    'ew_number': 'EWNumber',
    'ew_date_created': 'EWDateCreated',
    'edrpou': 'EDRPOU',
    'changed_data_ew': 'ChangedDataEW',
    'statement_of_acceptance_transfer_cargo_id': 'StatementOfAcceptanceTransferCargoID',
    'recipient_full_name_ew': 'RecipientFullNameEW',
    'ref_ew': 'RefEW',
    'block_international_sender_lkk': 'BlockInternationalSenderLKK',
    'can_ew_transporter': 'CanEWTransporter',
}


def to_pascal(string: str) -> str:
    if string in MANUAL_FIELD_NAMES:
        return MANUAL_FIELD_NAMES[string]

    return pascalize(string)


def to_camel(string: str) -> str:
    return camelize(string)


class PascalModel(BaseModel):
    class Config:
        alias_generator = to_pascal
        allow_population_by_field_name = True


class CamelModel(BaseModel):
    class Config:
        alias_generator = to_camel
