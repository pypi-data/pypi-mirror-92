import json
from xenqu._XenquBase import XenquBase

_prefix = '/files'

class FileRoutes:

    base: XenquBase

    def __init__(self, base: XenquBase) -> None:
        self.base = base


    """
    * Download File

    Parameters
    ----------
        tempHandleId: str
            temporary ID that represents the file to download

    ? @see [API Docs]{@link https://apidocs.xenqu.com/#2102ba3f-8a86-4f02-aeb2-3cdfbda3eadc}
    """
    def download(self, tempHandleId: str):
        data = self.base.makeGet(f"{_prefix}/{tempHandleId}", bytes=True)
        return data


    """
    * File uploads can be chunked or sent in one large chunk. Total file size can be 50Mb
    * fileHandle in the response represents the _temp_handle_id sent to other end points used to attach files to an object.
    * Uploads in predefined chunk sizes asynchronously for fast uploads
    
    Parameters
    ----------
        chunkData: str
        chunkSeq: int
        chunkStart: int
        chunkEnd: int
        chunkSize: int
        chunkLimit: int
        totalSize: int
        totalChunks: int

    ? @see [API Docs]{@link https://apidocs.xenqu.com/#aa314a75-2acb-42f9-9ff4-ad10282ee961}
    """
    def upload(self, chunkData: str, chunkSeq: int, chunkStart: int, chunkEnd: int, chunkSize: int, chunkLimit: int, totalSize: int, totalChunks: int):
        body = {
            "chunkData": chunkData,
            "chunkSeq": chunkSeq,
            "chunkStart": chunkStart,
            "chuckEnd": chunkEnd,
            "chunkSize": chunkSize,
            "chunkLimit": chunkLimit,
            "totalSize": totalSize,
            "totalChunks": totalChunks
        }

        data = self.base.makePost(f"{_prefix}", payload=json.dumps(body))
        return data