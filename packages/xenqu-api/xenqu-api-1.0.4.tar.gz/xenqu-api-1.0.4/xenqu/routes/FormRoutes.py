import json
from typing import Literal
from xenqu._XenquBase import XenquBase

_prefix = '/jform'

class FormRoutes:

    base: XenquBase

    def __init__(self, base: XenquBase) -> None:
        self.base = base


    """
    * Get form instance data tied to an item on a record

    Parameters
    ----------
        instanceId: int
            ID of a form instance

    ? @see [API Docs]{@link https://apidocs.xenqu.com/#140f933a-dc6d-404a-b072-9af30cb8cf57}
    """
    def getInstance(self, instanceId: int):
        data = self.base.makeGet(f"{_prefix}/instance/{instanceId}")
        return data


    """
    * Lock/Unlock Form

    Parameters
    ----------
        instanceId: int
            ID of a form instance

        action: Literal['lock', 'unlock', 'kick']
            action to perform on form instance

    ? @see [API Docs]{@link https://apidocs.xenqu.com/#7b50fc25-0966-41cd-ad28-47b6b803dec5}
    """
    def setLockStatus(self, instanceId: int, action: Literal['lock', 'unlock', 'kick']):

        if action == 'lock':
            body = {
                "override": True,
                "lock": True
            }
        elif action == 'unlock':
            body = {
                "unlock": True
            }
        else:
            body = {
                "kick": True
            }

        data = self.base.makePut(f"{_prefix}/instance/{instanceId}", payload=json.dumps(body))
        return data


    """
    * Update Field

    Parameters
    ----------
        instanceId: int
            ID of a form instance

        pageId: str
            ID of a specific page on the form

        stateId: str
            ID of the specific field on the form

        value: any
            new value of the field

        fieldId: str
            ID of the specific field on the form

    ? @see [API Docs]{@link https://apidocs.xenqu.com/#fd4f6a78-4cc3-4c34-bc2b-a072b0c4f937}
    """
    def setFieldValue(self, instanceId: int, pageId: str, stateId: str, value: any, fieldId: str):
        body = {
            "raw_value": value,
            "fid": fieldId
        }

        data = self.base.makePut(f"{_prefix}/instance/{instanceId}/page/{pageId}/field/{stateId}", payload=json.dumps(body))
        return data


    """
    * Request a form to be converted to PDF.
    * This is an asynchronous process and require polling the instance for the definition.pdf_id
    * to change values from before the call to this end point to after the call.
    * A 5 second polling interval is recommended.

    Parameters
    ----------
        instanceId: int
            ID of a form instance

        signPdf: bool
            To sign pdf or not to; (that is the question)
        
        addInfoFooter: bool
            To add an info footer or not to; (that is the question)

    ? @see [API Docs]{@link https://apidocs.xenqu.com/#267bf445-2cd4-4a9c-bbf5-d84252193c8e}
    """
    def generatePdf(self, instanceId: int, signPdf: bool, addInfoFooter: bool):
        body = {
            "signed_pdf": signPdf,
            "info_footer": addInfoFooter
        }

        data = self.base.makePost(f"{_prefix}/instance/{instanceId}/pdf/", payload=json.dumps(body))
        return data


    """
    * Files associated with a form can be downloaded by first requesting the file by its file id
    * which will return a temp id to use with the {@link FilesRoutes} 'downloadFile' to download the actual file.
    
    Parameters
    ----------
        instanceId: int
            ID of a form instance

        filesId: str
            ID of the file to retrieve

    ? @see [API Docs]{@link https://apidocs.xenqu.com/#6dd93321-6b80-4b74-af81-b2ccd0328478}
    """
    def getFormFile(self, instanceId: int, filesId: str):
        data = self.base.makeGet(f"{_prefix}/instance/{instanceId}/file/{filesId}")
        return data