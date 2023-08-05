
import json
from datetime import datetime
from typing import Any, OrderedDict

class OAuth2Token:

    def __init__(self, jsonData: str = None) -> None:
        self.token: str = ''
        self.tokenSecret: str = ''
        self.expires = datetime(year=1970, month=1, day=1, hour=0, minute=0, second=0)

        if jsonData:
            try:
                self.fromJson(json.loads(jsonData))
            except:
                raise Exception("## Invalid JSON format ##")

    def fromJson(self, json: OrderedDict[str, Any]):
        self.token = json["token"]
        self.tokenSecret = json["token_secret"]
        self.expires = datetime.fromtimestamp(json["expires"])