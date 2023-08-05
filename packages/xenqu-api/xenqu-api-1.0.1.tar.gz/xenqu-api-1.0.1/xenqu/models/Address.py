
import json

class Address:

    def __init__(
        self,
        order: int = 0,
        street1: str = '',
        street2: str = '',
        street3: str = '',
        region1: str = '',
        region2: str = '',
        postalcode: str = '',
        country: str = '',
        valid_from: str = '',
        valid_to: str = '',
        ) -> None:
        
        self.order = order
        self.street1 = street1
        self.street2 = street2
        self.street3 = street3
        self.region1 = region1
        self.region2 = region2
        self.postalcode = postalcode
        self.country = country
        self.valid_from = valid_from
        self.valid_to = valid_to

    def toDict(self):
        return {
            "order": self.order,
            "usage": "Address",
            "street1": self.street1,
            "street2": self.street2,
            "street3": self.street3,
            "region1": self.region1,
            "region2": self.region2,
            "postalcode": self.postalcode,
            "country": self.country,
            "valid_from": self.valid_from,
            "valid_to": self.valid_to
        }

    def toJson(self):
        return json.dumps(self.toDict())