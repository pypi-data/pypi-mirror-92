
import json
from typing import List

from .Item import Item

class Queue:

    def __init__(
        self,
        title: str = '',
        primary_actor_role_slug: str = 'worker',
        primary_actor_role: str = 'Worker',
        primary_actor_id: int = -1,
        section: int = 1,
        force_ordering: int = 0,
        progress_bin_id: int = None,

        items: List[Item] = [Item()]
        ) -> None:
        
        self.title = title
        self.primary_actor_role_slug = primary_actor_role_slug
        self.primary_actor_role = primary_actor_role
        self.primary_actor_id = primary_actor_id
        self.section = section
        self.force_ordering = force_ordering
        self.progress_bin_id = progress_bin_id
        self.items = items

    def toDict(self):
        return {
            "title": self.title,
            "primary_actor_role_slug": self.primary_actor_role_slug,
            "primary_actor_role": self.primary_actor_role,
            "primary_actor_id": self.primary_actor_id,
            "section": self.section,
            "force_ordering": self.force_ordering,
            "progress_bin_id": self.progress_bin_id,
            "items": [item.toDict() for item in self.items]
        }

    def toJson(self):
        return json.dumps(self.toDict())