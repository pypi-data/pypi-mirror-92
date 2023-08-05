from xenqu._XenquBase import XenquBase
from xenqu.routes.Tracking import _prefix

class RecordRoutes:

    base: XenquBase

    def __init__(self, base: XenquBase) -> None:
        self.base = base


    """
    * Get a record and its content on a specific tab

    Parameters
    ----------
        groupId: int

        contactId: int

    ? @see [API Docs]{@link https://apidocs.xenqu.com/#3bd6f73c-b25e-4d3f-8695-5e58d35df88d}
    """
    def getRecord(self, groupId: int, contactId: int):
        data = self.base.makeGet(f"{_prefix}/groups/{groupId}/actors/{contactId}")
        return data


    """
    * Initiates running automation rules on the record. This should be called after saving all queues or
    * editing any data that does not result in an item action (changing status, actors,etc)
    
    Parameters
    ----------
        groupId: int
        
        contactId: int

    ? @see [API Docs]{@link https://apidocs.xenqu.com/#f7b392bb-169b-4aca-b8d9-9cbafc471f9a}
    """
    def applyRules(self, groupId: int, contactId: int):
        data = self.base.makePost(f"{_prefix}/groups/{groupId}/actors/{contactId}/apply_rules")
        return data