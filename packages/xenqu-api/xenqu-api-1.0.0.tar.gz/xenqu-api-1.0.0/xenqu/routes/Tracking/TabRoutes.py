import json
from typing import List
from xenqu._XenquBase import XenquBase

from xenqu.routes.Tracking import _prefix

class TabRoutes:

    base: XenquBase

    def __init__(self, base: XenquBase) -> None:
        self.base = base


    """
    * Retrieve all contacts the current user can access within the scope of their tab membership, contact ownership, and task assignments
    
    Parameters
    ----------
        term: str
            search term for contact

        scope: List[str]
            search term scope

        count: int
            number of contacts to retrieve

        offset: int
            results offset

    ? @see [API Docs]{@link https://apidocs.xenqu.com/#7dab4692-f5f6-420d-9f46-dfc10c55e7d0}
    """
    def getContacts(self, term: str, scope: List[str], count: int, offset: int):
        params = {
            "term": term,
            "scope": scope,
            "count": count,
            "offset": offset
        }

        data = self.base.makeGet(f"{_prefix}/contacts", parameters=params)
        return data


    """
    * Get a list of tabs the current user is a member of

    ? @see [API Docs]{@link https://apidocs.xenqu.com/#764d0965-219e-41a0-b0cc-5896c39012c8}
    """
    def getTabs(self):
        data = self.base.makeGet(f"{_prefix}/groups")
        return data


    """
    * Get a list of all available items for a given tab that can be added to a record
    
    Parameters
    ----------
        groupId: int

    ? @see [API Docs]{@link https://apidocs.xenqu.com/#f89c6d8b-b7f6-48a2-9ab7-5ffc0029b326}
    """
    def getItems(self, groupId: int):
        data = self.base.makeGet(f"{_prefix}/groups/{groupId}/list/items")
        return data


    """
    * Get a list of predefined templates that can used to add content to a record

    Parameters
    ----------
        groupId: int

    ? @see [API Docs]{@link https://apidocs.xenqu.com/#c1386fb4-46fb-4934-91c4-e811f0fb56de}
    """
    def getQueueTemplates(self, groupId: int):
        data = self.base.makeGet(f"{_prefix}/groups/{groupId}/queue_templates")
        return data


    """
    * Load the predefined queues and items based on the template id
    
    Parameters
    ----------
        groupId: int

        templateId: str

    ? @see [API Docs]{@link https://apidocs.xenqu.com/#76dd3859-1f6f-479d-bd58-64b742cf8bdf}
    """
    def getQueueTemplate(self, groupId: int, templateId: str):
        data = self.base.makeGet(f"{_prefix}/groups/{groupId}/queue_templates/{templateId}")
        return data


    """
    * Get a list of all content libraries available on a tab
    
    Parameters
    ----------
        groupId: int

    ? @see [API Docs]{@link https://apidocs.xenqu.com/#2d7ae85c-9ea3-4832-83f5-14f982756c20}
    """
    def getLibraries(self, groupId: int):
        data = self.base.makeGet(f"{_prefix}/groups/{groupId}/libraries")
        return data


    """
    * Search for items and/or libraries by title

    Parameters
    ----------
        groupId: int

        title: str

    ? @see [API Docs]{@link https://apidocs.xenqu.com/#ee9ddc77-a8a6-49b7-a7d7-f9a72c44d00c}
    """
    def searchLibraries(self, groupId: int, title: str):
        body = {
            "title": title
        }

        data = self.base.makePost(f"{_prefix}/groups/{groupId}/libraries/select", payload=json.dumps(body))
        return data