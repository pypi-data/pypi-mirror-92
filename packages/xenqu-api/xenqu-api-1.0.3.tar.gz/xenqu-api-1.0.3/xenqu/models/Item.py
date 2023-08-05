import json
from typing import List

from .Actor import Actor

class Item:

    def __init__(
        self,
        order: int = 0,
        tracking_id: int = 1,
        item_id: int = -1,
        tracking_library_id: int = -1,
        
        actors: List[Actor] = []
        ) -> None:
        
        self.order = order
        self.tracking_id = tracking_id
        self.item_id = item_id
        self.tracking_library_id = tracking_library_id
        self.actors = actors

    def toDict(self):
        return {
            "order": self.order,
            "tracking_id": self.tracking_id,
            "item_id": self.item_id,
            "tracking_library_id": self.tracking_library_id,
            "item": {
                "actors": [actor.toDict() for actor in self.actors]
            }
        }

    def toJson(self):
        return json.dumps(self.toDict())
