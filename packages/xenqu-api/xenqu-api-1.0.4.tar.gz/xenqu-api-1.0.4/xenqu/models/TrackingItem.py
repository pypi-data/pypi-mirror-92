import json
import datetime

from typing import List, Literal, Optional, Union

from .Actor import Actor

class TrackingItem:

    def _is_valid_extra_label(self, s: str):
        if len(s) > 35:
            raise ValueError("The Extra Label property must not be longer than 35 characters.")
        return s

    def __init__(
        self,
        status: Literal["open", "closed", "skip"] = "open",
        schedule_date: Union[Literal[None], datetime.date] = None,
        priority: Literal[1, 2, 3] = 2,
        extra_label: str = '',
        
        actors: Optional[List[Actor]] = [Actor()]
        ) -> None:
        
        self.status = status
        self.schedule_date = schedule_date
        self.priority = priority
        self.extra_label = self._is_valid_extra_label(extra_label)
        self.actors = actors


    def toDict(self):
        return {
            "status": self.status,
            "schedule_date": self.schedule_date,
            "priority": self.priority,
            "extra_label": self.extra_label,
            "item": {
                "actors": [actor.toDict() for actor in self.actors] if self.actors != None else None
            }
        }

    def toJson(self):
        return json.dumps(self.toDict())