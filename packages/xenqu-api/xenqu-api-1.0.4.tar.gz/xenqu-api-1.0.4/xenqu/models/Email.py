import json

class Email:

    def __init__(
        self,
        order: int = 0,
        address: str = ''
        ) -> None:
        
        self.order = order
        self.address = address

    def toDict(self):
        return {
            "order": self.order,
            "usage": "Email",
            "address": self.address
        }

    def toJson(self):
        return json.dumps(self.toDict())
