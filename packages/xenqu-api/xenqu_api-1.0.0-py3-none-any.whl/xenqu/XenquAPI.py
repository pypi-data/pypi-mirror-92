
from xenqu._XenquBase import XenquBase
from xenqu.routes import AccountRoutes, ContactRoutes, TrackingRoutes, FormRoutes, ReportRoutes, FileRoutes, SearchRoutes

class XenquAPI:
    
    def __init__(
        self,
        clientId: str, 
        clientSecret: str, 
        pemPrivateKey: bytes, 
        subscriber: str, 
        baseUrl: str = 'https://xenqu.com/api') -> None:
        
        self.clientId = clientId
        self.clientSecret = clientSecret
        self.pemPrivateKey = pemPrivateKey
        self.subscriber = subscriber
        self.baseUrl = baseUrl

        self.base = XenquBase(baseUrl=self.baseUrl, clientId=self.clientId, clientSecret=self.clientSecret)
        self.isInit: bool = False

        self.account = AccountRoutes(self.base)
        self.contact = ContactRoutes(self.base)
        self.tracking = TrackingRoutes(self.base)
        self.forms = FormRoutes(self.base)
        self.reports = ReportRoutes(self.base)
        self.files = FileRoutes(self.base)
        self.search = SearchRoutes(self.base)

        self.init()

    def init(self) -> None:
        if not self.isInit:
            return self.reauth()
        else:
            raise Exception("Already Initiated")

    def reauth(self) -> None:
        self.isInit = False
        token = self.base.makeOauth2Request(self.pemPrivateKey)
        self.base.updateOauth(token)
        self._updateRoutes()
        self.isInit = True

    def _updateRoutes(self) -> None:
        self.account.base = self.base
        self.contact.base = self.base
        
        self.tracking.base = self.base
        self.tracking.update()

        self.forms.base = self.base
        self.reports.base = self.base
        self.files.base = self.base
        self.search.base = self.base