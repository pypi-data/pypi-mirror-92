
from xenqu._XenquBase import XenquBase
from xenqu.routes.Tracking import TabRoutes, RecordRoutes, QueueRoutes, ItemRoutes

class TrackingRoutes:

    def __init__(self, base: XenquBase) -> None:
        self.base = base

        self.tabs = TabRoutes(self.base)
        self.records = RecordRoutes(self.base)
        self.queues = QueueRoutes(self.base)
        self.items = ItemRoutes(self.base)

    def update(self):
        self.tabs.base = self.base
        self.records.base = self.base
        self.queues.base = self.base
        self.items.base = self.base