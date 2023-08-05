from xenqu._XenquBase import XenquBase
from xenqu.models import Contact

_prefix = '/contact'

class ContactRoutes:

    base: XenquBase

    def __init__(self, base: XenquBase) -> None:
        self.base = base


    """
    * The preferred end point for accessing contacts is tracking/contacts.
    * This end point only returns contacts created by the current user.
    * Refer to that documentation for options.

    Parameters
    ----------
        term: str
            search term
        
    ? @see [API Docs]{@link https://apidocs.xenqu.com/#e0fbbe9f-1ae3-4523-adff-ea8506ce7e0a}
    """
    def searchContacts(self, term: str):
        data = self.base.makeGet(f"{_prefix}?term={term}")
        return data


    """
    * Get full details on a contact

    Parameters
    ----------
        contactId: int
            ID of the contact to retrieve

    ? @see [API Docs]{@link https://apidocs.xenqu.com/#24bb22da-7e96-4c16-8c32-c4bca1aeed86}
    """
    def getContactDetail(self, contactId: int):
        data = self.base.makeGet(f"{_prefix}/{contactId}")
        return data


    """
    * Add a new contact. Returns created contact.

    Parameters
    ----------
        contact: Contact
            contact data to add

    ? @see [API Docs]{@link https://apidocs.xenqu.com/#7969a360-ee09-41a8-9299-05a5f0ffb7fb}
    """
    def addContact(self, contact: Contact):
        data = self.base.makePost(f"{_prefix}", payload=contact.toJson())
        return data


    """
    * Edit a contact. Returns edited contact.

    Parameters
    ----------
        contactId: int
            ID of the contact to edit

        contact: Contact
            contact data to modify

    ? @see [API Docs]{@link https://apidocs.xenqu.com/#7ef9b643-8086-4ca0-ad5c-05895dc3eb52}
    """
    def editContact(self, contactId: int, contact: Contact):
        data = self.base.makePut(f"{_prefix}/{contactId}", payload=contact.toJson())
        return data


    """
    * Delete a contact. Returns deleted contact id.

    Parameters
    ----------
        contactId: int
            ID of the contact to delete

    ? @see [API Docs]{@link https://apidocs.xenqu.com/#027b6abb-2ac1-40dc-a82c-afe4a631aae3}
    """
    def deleteContact(self, contactId: int):
        data = self.base.makeDelete(f"{_prefix}/{contactId}")
        return data