from xenqu._XenquBase import XenquBase

_prefix = '/search'

class SearchRoutes:

    base: XenquBase

    def __init__(self, base: XenquBase) -> None:
        self.base = base