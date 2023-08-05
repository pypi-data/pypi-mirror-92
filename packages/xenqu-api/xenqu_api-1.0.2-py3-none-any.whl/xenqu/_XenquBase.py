
import time
import requests
import jwt
from jwcrypto import jwk, jwt
from requests_oauthlib import OAuth1
from xenqu.models import OAuth2Token

class XenquBase:

    def __init__(self, baseUrl: str, clientId: str = '', clientSecret: str = '') -> None:
        self.baseUrl = baseUrl
        self.clientId = clientId
        self.clientSecret = clientSecret

        self.apiUrl = self.baseUrl + '/api'
        self.oauth = OAuth2Token()


    """
    * Update Oath Paramaters
    
    Parameters
    ----------
        oauth: OAuth2Token
            Oauth Token Information
    """
    def updateOauth(self, oauth: OAuth2Token):
        self.oauth = oauth


    """
    * Perform {GET} request

    Parameters
    ----------
        path: str
            suffix url for api call

        paramaters: dict
            inline request parameters
    """
    def makeGet(self, path: str, parameters: dict = None, bytes: bool = False):
        url = self.apiUrl + path

        oauth = OAuth1(client_key=self.clientId, client_secret=self.clientSecret, resource_owner_key=self.oauth.token, resource_owner_secret=self.oauth.tokenSecret)
        res = requests.get(url=url, params=parameters, auth=oauth)

        if res.status_code in range(200, 211):
            if bytes:
                return res.content
            else:
                return res.text
        else:
            raise Exception(f"Error at OAuth 2.0 Endpoint: {res.content}\nURL: {res.url}\nBody: {res.request.body}\nStatus Code: {res.status_code}")


    """
    * Perform {POST} request

    Parameters
    ----------
        path: str
            suffix url for api call

        payload: str
            body of the request

        paramaters: dict
            inline request parameters
    """
    def makePost(self, path: str, payload: str = '{}'):
        url = self.apiUrl + path

        oauth = OAuth1(client_key=self.clientId, client_secret=self.clientSecret, resource_owner_key=self.oauth.token, resource_owner_secret=self.oauth.tokenSecret)
        res = requests.post(url=url, data=payload, headers={"Content-Type": "application/json"}, auth=oauth)

        if res.status_code > 199 and res.status_code < 210:
            return res.text
        else:
            raise Exception(f"Error at OAuth 2.0 Endpoint: {res.content}\nURL: {res.url}\nBody: {res.request.body}\nStatus Code: {res.status_code}")


    """
    * Perform {PUT} request

    Parameters
    ----------
        path: str
            suffix url for api call

        payload: str
            body of the request

        paramaters: dict
            inline request parameters
    """
    def makePut(self, path: str, payload: str):
        url = self.apiUrl + path

        oauth = OAuth1(client_key=self.clientId, client_secret=self.clientSecret, resource_owner_key=self.oauth.token, resource_owner_secret=self.oauth.tokenSecret)
        res = requests.put(url=url, data=payload, headers={"Content-Type": "application/json"}, auth=oauth)

        if res.status_code > 199 and res.status_code < 210:
            print(f"Body: {res.request.body}")
            return res.text
        else:
            raise Exception(f"Error at OAuth 2.0 Endpoint: {res.content}\nURL: {res.url}\nBody: {res.request.body}\nStatus Code: {res.status_code}")


    """
    * Perform {DELETE} request

    Parameters
    ----------
        path: str
            suffix url for api call

        payload: str
            body of the request

        paramaters: dict
            inline request parameters
    """
    def makeDelete(self, path: str, payload: str = None, paramaters: dict = None):
        url = self.apiUrl + path

        oauth = OAuth1(client_key=self.clientId, client_secret=self.clientSecret, resource_owner_key=self.oauth.token, resource_owner_secret=self.oauth.tokenSecret)
        res = requests.delete(url=url, data=payload, headers={"Content-Type": "application/json"}, auth=oauth)

        if res.status_code > 199 and res.status_code < 210:
            return res.text
        else:
            raise Exception(f"Error at OAuth 2.0 Endpoint: {res.content}\nURL: {res.url}\nBody: {res.request.body}\nStatus Code: {res.status_code}")


    """
    * Does the Oauth stuff

    Parameters
    ----------
        pemPrivateKey: bytes
            raw bytes from reading the pem file
    """
    def makeOauth2Request(self, pemPrivateKey: bytes) -> OAuth2Token:
        key = jwk.JWK.from_pem(pemPrivateKey)
        payload = {
            "exp": time.time() + 300,
            "iss": self.clientId,
            "aud": self.baseUrl,
            "sub": "5f3ed190c32e5f000186bb76"
        }

        raw_jwt_token = jwt.JWT(header={"alg": "RS256"}, claims=payload)
        raw_jwt_token.make_signed_token(key)

        signed_token = raw_jwt_token.serialize()

        payload_data = f'grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Ajwt-bearer&assertion={signed_token}'

        oauth_url = self.apiUrl + '/oauth2/token'
        res = requests.post(url=oauth_url, data=payload_data, auth=(self.clientId, self.clientSecret))

        if res.status_code in range(200, 211):
            return OAuth2Token(res.text)
        else:
            raise Exception(f"## Error with OAuth 2.0 Request ##\n\tStatus Code: {res.status_code}\n\tResponse: {res.text}")
