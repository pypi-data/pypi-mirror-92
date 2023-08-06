import enum


class CounterpartyProperty(str, enum.Enum):
    SENDER = 'Sender'
    RECIPIENT = 'Recipient'
    THIRDPERSON = 'ThirdPerson'

    def __json__(self):
        return self.value
