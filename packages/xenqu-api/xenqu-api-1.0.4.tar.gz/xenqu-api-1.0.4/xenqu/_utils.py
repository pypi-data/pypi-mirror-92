
from typing import Any, Dict

import json
import base64
import requests
from requests.models import Response



def b64EncodeBytes(b: bytes) -> str:
    return base64.b64encode(b).decode('ascii')

def performGet(url: str, headers: Dict[str, Any]) -> Response:
    return requests.get(url=url, headers=headers)

def performPost(url: str, headers: Dict[str, Any], jsonData: dict) -> Response:
    return requests.post(url=url, headers=headers, json=json.loads(jsonData))

def performPut(url: str, headers: Dict[str, Any], jsonData: dict) -> Response:
    return requests.put(url=url, headers=headers, json=json.loads(jsonData))

def performDelete(url: str, headers: Dict[str, Any], jsonData: dict) -> Response:
    return requests.delete(url=url, headers=headers, json=json.loads(jsonData))