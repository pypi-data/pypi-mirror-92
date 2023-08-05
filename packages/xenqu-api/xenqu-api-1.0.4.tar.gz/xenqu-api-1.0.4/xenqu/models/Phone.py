import json

class Phone:

    def __init__(
        self,
        order: int = 0,
        format: str = '',
        number: str = ''
        ) -> None:
        
        self.order = order
        self.format = format
        self.number = number

    def toDict(self):
        return {
            "order": self.order,
            "usage": "Phone",
            "format": self.format,
            "number": self.number
        }

    def toJson(self):
        return json.dumps(self.toDict())