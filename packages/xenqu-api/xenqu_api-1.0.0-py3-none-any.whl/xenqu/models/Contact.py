import json
from typing import List

from .Address import Address
from .Email import Email
from .Phone import Phone

class Contact:

    def __init__(
        self,
        display_name: str = '',
        org_name: str = '',
        title: str = '',
        salutation: str = '',
        first_name: str = '',
        middle_name: str = '',
        last_name: str = '',
        name_suffix: str = '',
        nick_name: str = '',
        notes: str = '',
        
        emails: List[Email] = [Email(order=0)],
        phones: List[Phone] = [Phone(order=0)],
        addresses: List[Address] = [Address(order=0)],

        tags: List[str] = []
        ) -> None:
        
        self.display_name = display_name
        self.org_name = org_name
        self.title = title
        self.salutation = salutation
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.name_suffix = name_suffix
        self.nick_name = nick_name
        self.notes = notes
        self.emails = emails
        self.phones = phones
        self.addresses = addresses
        self.tags = tags

    def toDict(self):
        return {
            "display_name": self.display_name,
            "org_name": self.org_name,
            "title": self.title,
            "salutation": self.salutation,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "name_suffix": self.name_suffix,
            "nick_name": self.nick_name,
            "notes": self.notes,
            "emails": [email.toDict() for email in self.emails],
            "phones": [phone.toDict() for phone in self.phones],
            "addresses": [address.toDict() for address in self.addresses],
            "tags": self.tags
        }

    def toJson(self):
        return json.dumps(self.toDict())
