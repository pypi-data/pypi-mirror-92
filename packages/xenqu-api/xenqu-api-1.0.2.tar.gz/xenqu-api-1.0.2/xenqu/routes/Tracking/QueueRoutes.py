from xenqu._XenquBase import XenquBase
from xenqu.models import Queue
from xenqu.routes.Tracking import _prefix

class QueueRoutes:

    base: XenquBase

    def __init__(self, base: XenquBase) -> None:
        self.base = base


    """
    * Get the latest values for a queue including all its items.
    
    Parameters
    ----------
        groupId: int

        queueId: int

    ? @see [API Docs]{@link https://apidocs.xenqu.com/#bc053d06-4bbd-4c47-9c09-7db3454d16bd}
    """
    def getQueue(self, groupId: int, queueId: int):
        data = self.base.makeGet(f"{_prefix}/groups/{groupId}/queues/{queueId}")
        return data


    """
    * Create a queue

    Parameters
    ----------
        groupId: int

        queue: Queue
            queue to add

    ? @see [API Docs]{@link https://apidocs.xenqu.com/#38e912b5-5c85-47f7-9800-299c5d66e773}
    """
    def addQueue(self, groupId: int, queue: Queue):
        data = self.base.makePost(f"{_prefix}/groups/{groupId}/queues", payload=queue.toJson())
        return data


    """
    * Edit a queue

    Parameters
    ----------
        groupId: int

        queueId: int
            ID of the queue to modify

        queue: Queue
            new queue data

    ? @see [API Docs]{@link https://apidocs.xenqu.com/#9c87cc46-1abb-4c76-a973-4ad3a8e5aec9}
    """
    def editQueue(self, groupId: int, queueId: int, queue: Queue):
        data = self.base.makePut(f"{_prefix}/groups/{groupId}/queues/{queueId}", payload=queue.toJson())
        return data


    """
    * Delete a queue
    
    Parameters
    ----------
        groupId: int

        queueId: int

    ? @see [API Docs]{@link https://apidocs.xenqu.com/#de5d65c9-0d96-4b7a-8436-f0a450b21e5f}
    """
    def deleteQueue(self, groupId: int, queueId: int):
        data = self.base.makeDelete(f"{_prefix}/groups/{groupId}/queues/{queueId}")
        return data