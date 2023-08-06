from typing import TYPE_CHECKING

import pytest
from novaposhta.const import CounterpartyProperty
from novaposhta.exceptions import InvalidDataError
from novaposhta.schemas import (
    Counterparty as CounterpartySchema, CounterpartyAddress, OrganizationBody,
    SenderBody, ThirdpartyBody, UpdateCounterpartyBody, ContactPerson
)
from novaposhta.schemas.counterparties import CounterpartyContactPersonSaveBody, CounterpartyContactPersonUpdateBody

if TYPE_CHECKING:  # pragma: no cover
    from novaposhta.client import Novaposhta


def test_counterparties_list(client: 'Novaposhta'):
    counterparties = client.counterparties().list()
    assert len(counterparties) >= 1
    assert isinstance(counterparties[0], CounterpartySchema)

    recipient_counterparties = client.counterparties().list(counterparty_property='Recipient')
    assert len(counterparties) >= 1
    assert isinstance(counterparties[0], CounterpartySchema)

    third_counterparties = client.counterparties().list(counterparty_property='ThirdPerson')
    assert third_counterparties != recipient_counterparties

    found_counterparties = client.counterparties().list(find_by_string=counterparties[0].description)
    assert len(counterparties) >= 1
    assert found_counterparties == counterparties


def test_counterparties_get_addresses(client: 'Novaposhta'):
    counterparties = client.counterparties().list()
    addresses = client.counterparties().get_addresses(counterparties[0].ref)

    assert len(addresses) >= 1
    assert type(addresses[0]) == CounterpartyAddress

    counterparties = client.counterparties().list()
    recipient_addresses = client.counterparties().get_addresses(counterparties[0].ref, CounterpartyProperty.RECIPIENT)
    assert len(recipient_addresses) >= 1


def test_counterparties_save(client: 'Novaposhta'):
    counterparty = client.counterparties().save(
        body=OrganizationBody(edrpou="123456789")
    )
    assert counterparty.ref is not None
    client.counterparties().delete(counterparty.ref)

    city = client.addresses().get_cities(limit=1)[0]
    counterparty = client.counterparties().save(
        body=ThirdpartyBody(edrpou="123456789", city_ref=city.ref)
    )
    assert counterparty.ref is not None
    client.counterparties().delete(counterparty.ref)

    with pytest.raises(InvalidDataError):
        counterparty = client.counterparties().save(
            body=SenderBody(
                first_name='фы',
                middle_name='фы',
                last_name='фы',
                phone='+380663333333',
                email='ad@ad.ad',
                counterparty_property=CounterpartyProperty.SENDER
            )
        )


def test_counterparties_update(client: 'Novaposhta'):
    counterparty = client.counterparties().save(
        body=OrganizationBody(edrpou="123456789")
    )
    assert counterparty.ref is not None
    city = client.addresses().get_cities(limit=1)[0]

    # Can't edit data of legal person
    with pytest.raises(InvalidDataError):
        counterparty = client.counterparties().update(body=UpdateCounterpartyBody(
            ref=counterparty.ref, city_ref=city.ref, first_name='12', last_name='123', phone='123',
            edrpou="123456789",
            email='13', counterparty_type='Organization', counterparty_property=CounterpartyProperty.THIRDPERSON
        ))

    client.counterparties().delete(counterparty.ref)

    city = client.addresses().get_cities(limit=1)[0]
    counterparty = client.counterparties().save(
        body=ThirdpartyBody(edrpou="123456789", city_ref=city.ref)
    )

    # Can't edit data of legal person
    with pytest.raises(InvalidDataError):
        counterparty = client.counterparties().update(
            body=UpdateCounterpartyBody(
                ref=counterparty.ref, city_ref=city.ref, first_name='12',
                ownership_form='7f0f351d-2519-11df-be9a-000c291af1b3',
                counterparty_type='Organization', counterparty_property=CounterpartyProperty.RECIPIENT

            )
        )
    counterparty = client.counterparties().save(
        body=SenderBody(
            first_name='фы',
            middle_name='фы',
            last_name='фы',
            phone='+380663333333',
            email='ad@ad.ad',
            # counterparty_property=''
            counterparty_property=CounterpartyProperty.RECIPIENT
        )
    )

    counterparty = client.counterparties().update(
        body=UpdateCounterpartyBody(
            ref=counterparty.ref, phone='0663333333', first_name='апра', last_name='выав',
            city_ref=city.ref, counterparty_property=CounterpartyProperty.THIRDPERSON,
            counterparty_type='PrivatePerson',
        )
    )
    assert counterparty.first_name == 'Апра'
    assert counterparty.last_name == 'Выав'

    # Counterparty PrivatePerson can't be deleted
    with pytest.raises(InvalidDataError):
        client.counterparties().delete(counterparty.ref)


def test_counterparties_options(client: 'Novaposhta'):
    counterparty = client.counterparties().list(limit=1)[0]
    options = client.counterparties().get_options(ref=counterparty.ref)
    assert len(options) >= 1


def test_counterparties_get_contact_persons(client: 'Novaposhta'):
    counterparty = client.counterparties().list(limit=1)[0]
    contact_persons = client.counterparties().get_contact_persons(ref=counterparty.ref)
    assert len(contact_persons) >= 1


def test_contact_person_save(client: 'Novaposhta'):
    counterparty = client.counterparties().list(limit=1)[0]

    body = CounterpartyContactPersonSaveBody(
        counterparty_ref=counterparty.ref,
        first_name='Алекс',
        middle_name='Алекс',
        last_name='Алекс',
        phone='380663333333',
    )
    # ContactPerson already exist for Sender
    with pytest.raises(InvalidDataError):
        contact_person = client.contact_persons().save(body=body)
    # assert type(contact_person) == ContactPerson
    # client.contact_persons().delete(contact_person.ref)


def test_contact_person_update(client: 'Novaposhta'):
    counterparty = client.counterparties().list(limit=1)[0]
    contact_person = client.counterparties().get_contact_persons(ref=counterparty.ref)[0]

    body = CounterpartyContactPersonUpdateBody(
        counterparty_ref=counterparty.ref,
        ref=contact_person.ref,
        first_name='Алекс',
        middle_name='Алекс',
        last_name='Алекс',
        phone='380663333333',
    )
    # 'Changing own phone number is not allowed', 'Edit disabled for PrivatePerson Sender'
    with pytest.raises(InvalidDataError):
        contact_person = client.contact_persons().update(body=body)


def test_contact_person_delete(client: 'Novaposhta'):
    counterparty = client.counterparties().list(limit=1)[0]
    contact_person = client.counterparties().get_contact_persons(ref=counterparty.ref)[0]

    # Loyalty user can not delete contact person
    with pytest.raises(InvalidDataError):
        contact_person = client.contact_persons().delete(ref=contact_person.ref)
