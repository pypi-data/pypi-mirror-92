import json

class Actor:

    def __init__(
        self,
        order: int = 0,
        contact_id: int = 0,
        actor_role: str = 'Worker',
        actor_role_slug: str = 'worker',
        status: str = None
        ) -> None:

        self.order = order
        self.contact_id = contact_id
        self.actor_role = actor_role
        self.actor_role_slug = actor_role_slug
        self.status = status

    def toDict(self):
        return {
            "order": self.order,
            "contact_id": self.contact_id,
            "actor_role": self.actor_role,
            "actor_role_slug": self.actor_role_slug,
            "status": self.status
        }

    def toJson(self):
        return json.dumps(self.toDict())
