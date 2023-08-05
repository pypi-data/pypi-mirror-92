from xenqu._XenquBase import XenquBase

_prefix = '/user'

class AccountRoutes:

    base: XenquBase

    def __init__(self, base: XenquBase) -> None:
        self.base = base


    """
    * Gets the Current API User's Information

    ? @see [API Docs]{@link https://apidocs.xenqu.com/#3e68223a-c6a6-4469-b2be-5a43315c7210}
    """
    def getUserInfo(self):
        data = self.base.makeGet(f'{_prefix}/info')
        return data