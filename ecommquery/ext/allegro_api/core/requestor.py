from enum import Enum
import base64
import requests

from ecommquery.ext.allegro_api.lib.constants import BASE_URL, BASE_URL_SANDBOX, PathTo, API_BASE_URL_SANDBOX


class Requestor:

    def __init__(self, client_id, client_secret, sandbox: bool = False):
        # Create Basic Auth header manually (same as curl)
        credentials = f"{client_id}:{client_secret}"
        b64_credentials = base64.b64encode(credentials.encode()).decode()

        self.client_id = client_id
        self.headers = {
            "Authorization": f"Basic {b64_credentials}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        
        if not sandbox:
            self._base_url = BASE_URL
        else: 
            self._base_url = BASE_URL_SANDBOX

    def isSandBox(self):
        return self._base_url == BASE_URL_SANDBOX

    def post(self, request_to: PathTo, params):
        return requests.post(
            self._base_url + request_to.getPath(),
            headers=self.headers,
            params=params
        )

    def getSessionRequestor(self, access_token:str):
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.allegro.public.v1+json"
        }

        return (lambda path: requests.get(API_BASE_URL_SANDBOX + path, headers=headers),
                lambda path, params: requests.post(API_BASE_URL_SANDBOX + path, headers=headers, params=params))
