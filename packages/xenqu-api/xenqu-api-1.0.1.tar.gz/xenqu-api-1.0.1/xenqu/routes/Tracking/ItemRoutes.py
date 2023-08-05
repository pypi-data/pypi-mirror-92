import json
from typing import Literal
from xenqu._XenquBase import XenquBase
from xenqu.models import TrackingItem

from xenqu.routes.Tracking import _prefix

class ItemRoutes:

    base: XenquBase

    def __init__(self, base: XenquBase) -> None:
        self.base = base


    """
    * Get list of items for current user. This data is the same as seen under the "My Queue" menu in the UI. queued now complete

    Parameters
    ----------
        queued: Literal["open", "closed"] = "open"
            item queue status

        sortBy: Literal["relevance", "create_date", "last_log_date", "schedule_date", "priority", "item_title"] = "last_log_date"
            sort options

        descending: bool = True
            sort order

        offset: int = 0
            sort offset

        count: int = 20
            number of results to retrieve

    ? @see [API Docs]{@link https://apidocs.xenqu.com/#96bd981d-1505-4353-86f7-35f17d5a2f69}
    """
    def getAssignedItemList(self, queued: Literal["open", "closed"] = "open", sortBy: Literal["relevance", "create_date", "last_log_date", "schedule_date", "priority", "item_title"] = "last_log_date", descending: bool = True, offset: int = 0, count: int = 20):

        params = {
            "queued": queued,
            "sortby": sortBy,
            "offset": offset,
            "count": count
        }

        if descending:
            params["sortby"] = params["sortby"] + ',desc'
            data = self.base.makeGet(f"{_prefix}/user/items", parameters=params)

        else:
            data = self.base.makeGet(f"{_prefix}/user/items", parameters=params)

        return data


    """
    * Get more details about an item assigned to the current user. Includes the complete activity log on the item.

    Parameters
    ----------
        trackingId: int
            tracking ID to retrieve details from

    ? @see [API Docs]{@link https://apidocs.xenqu.com/#c909077e-1ac7-4501-9b0b-626d8bd75694}
    """
    def getAssignedItemDetail(self, trackingId: int):
        data = self.base.makeGet(f"{_prefix}/user/items/{trackingId}")
        return data


    """
    * Get detail about a tracking item on a record

    Parameters
    ----------
        groupId: int

        queueId: int

        trackingId: int

    ? @see [API Docs]{@link https://apidocs.xenqu.com/#9b97b262-1934-449f-9660-81770f6385f3}
    """
    def getTrackingItem(self, groupId: int, queueId: int, trackingId: int):
        data = self.base.makeGet(f"{_prefix}/groups/{groupId}/queues/{queueId}/items/{trackingId}")
        return data


    """
    * Update a tracking item on a record

    Parameters
    ----------
        groupId: int

        queueId: int

        trackingId: int

        trackingItem: TrackingItem

    ? @see [API Docs]{@link https://apidocs.xenqu.com/#16602514-0065-4db4-8327-1c15338579fb}
    """
    def updateTrackingItem(self, groupId: int, queueId: int, trackingId: int, trackingItem: TrackingItem):
        data = self.base.makePut(f"{_prefix}/groups/{groupId}/queues/{queueId}/items/{trackingId}", payload=trackingItem.toJson())
        return data


    """
    * This will post a message on the item which is visible to all actors in their My Queue view,
    * on the dashboard, and, if subscribed, email/text to each assigned actor.
    
    Parameters
    ----------
        trackingId: int
            tracking ID of the item

        messageText: str
            message to add to item

    ? @see [API Docs]{@link https://apidocs.xenqu.com/#e3c14915-4491-4b37-a381-0af2d2ef10ce}
    """
    def addMessage(self, trackingId: int, messageText: str):
        body = {
            "event_data": {
                "message_text": messageText
            }
        }
        
        data = self.base.makePost(f"{_prefix}/items/{trackingId}/logs", payload=json.dumps(body))
        return data


    """
    * Set a callback with a url to post back against when anything changes on the given item.
    
    Parameters
    ----------
        groupId: int

        queueId: int

        trackingId: int

        callbackUrl: str

    ? @see [API Docs]{@link https://apidocs.xenqu.com/#bda9a19c-f79f-466e-b47b-b230bda2b3e4}
    """
    def setCallback(self, groupId: int, queueId: int, trackingId: int, callbackUrl: str):
        body = {
            "callback_url": callbackUrl
        }

        data = self.base.makePut(f"{_prefix}/groups/{groupId}/queues/{queueId}/items/{trackingId}/callback", payload=json.dumps(body))
        return data


    """
    * Remove callback previously set on an item

    Parameters
    ----------
        groupId: int

        queueId: int

        trackingId: int

        callbackUrl: str

    ? @see [API Docs]{@link https://apidocs.xenqu.com/#2ce6d984-d018-464d-a024-a116f04d9e05}
    """
    def unsetCallback(self, groupId: int, queueId: int, trackingId: int, callbackUrl: str):
        body = {
            "callback_url": callbackUrl
        }

        data = self.base.makeDelete(f"{_prefix}/groups/{groupId}/queues/{queueId}/items/{trackingId}/callback", payload=json.dumps(body))
        return data


    """
    * By tab, get a list of items ordered by most recent activity to oldest

    Parameters
    ----------
        groupId: int

        count: int
            number of items to retrieve

        offset: int
            data offset

    ? @see [API Docs]{@link https://apidocs.xenqu.com/#b0730376-afa6-4831-806d-5c54411e6ff7}
    """
    def getActivityStream(self, groupId: int, count: int, offset: int):
        params = {
            "count": count,
            "offset": offset
        }

        data = self.base.makeGet(f"{_prefix}/groups/{groupId}/items/activity", parameters=params)
        return data


    """
    * For tracking items of type "attachment", list all the files associated with the item

    Parameters
    ----------
        trackingId: int
            tracking ID of the item to get attachments from

    ? @see [API Docs]{@link https://apidocs.xenqu.com/#cd32010b-15e7-4287-aa8d-4e81645eec3d}
    """
    def getListAttachments(self, trackingId: int):
        data = self.base.makeGet(f"{_prefix}/attachments/{trackingId}")
        return data


    """
    * For tracking items of type "attachment", list all the files associated with the item

    Parameters
    ----------
        attachmentId: str
            ID of the attachment to download

        filesId: str

    ? @see [API Docs]{@link https://apidocs.xenqu.com/#cd32010b-15e7-4287-aa8d-4e81645eec3d}
    """
    def getDownloadAttachment(self, attachmentId: str, filesId: str):
        data = self.base.makeGet(f"{_prefix}/attachments/{attachmentId}/files/{filesId}")
        return data


    """
    * For tracking items of type "attachment", list all the files associated with the item

    Parameters
    ----------
        trackingId: int

        tempHandleId: str

        attachmentId: str

        contentType: str

        fileName: str

        order: str

        filesId: str

    ? @see [API Docs]{@link https://apidocs.xenqu.com/#db3c24c6-a6d7-4f44-8eb3-9a82b70753e3}
    """
    def addAttachment(self, trackingId: int, tempHandleId: str, attachmentId: str, contentType: str, fileName: str, order: int, filesId: str = None):
        body = {
            "tracking_id": trackingId,
            "attachment_id": attachmentId,
            "files_id": filesId,
            "content_type": contentType,
            "filename": fileName,
            "order": order,
            "_temp_handle_id": tempHandleId
        }

        data = self.base.makePost(f"{_prefix}/attachments/{attachmentId}/files", payload=json.dumps(body))
        return data


    """
    * For tracking items of type "attachment", list all the files associated with the item
    
    Parameters
    ----------
        trackingId: int

        attachmentId: str

        filesId: str

        contentType: str

        fileName: str

        order: int

        tempHandleId: str

    ? @see [API Docs]{@link https://apidocs.xenqu.com/#0b52cc8c-40e4-40d6-8b95-266f7c8f139d}
    """
    def updateAttachment(self, trackingId: int, attachmentId: str, filesId: str, contentType: str, fileName: str, order: int, tempHandleId: str):
        body = {
            "tracking_id": trackingId,
            "attachment_id": attachmentId,
            "files_id": filesId,
            "content_type": contentType,
            "filename": fileName,
            "order": order,
            "_temp_handle_id": tempHandleId
        }

        data = self.base.makePut(f"{_prefix}/attachments/{attachmentId}/files/{filesId}", payload=json.dumps(body))
        return data


    """
    * For tracking items of type "attachment", list all the files associated with the item
    
    Parameters
    ----------
        attachmentId: str
            ID of the attachment to delete

        filesId: str

    ? @see [API Docs]{@link https://apidocs.xenqu.com/#2026a2a1-5455-4e60-a782-649b8101b7e2}
    """
    def deleteAttachment(self, attachmentId: str, filesId: str):
        data = self.base.makeDelete(f"{_prefix}/attachments/{attachmentId}/files/{filesId}")
        return data

    