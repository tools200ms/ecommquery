
import base64

import requests

from ecommquery.ext.allegro_api.lib.constants import (BASE_URL,
                                                      BASE_URL_SANDBOX,
                                                      API_BASE_URL,
                                                      API_BASE_URL_SANDBOX,
                                                      PathTo)


class Requestor:

    def __init__(self, client_id, client_secret, options, sandbox: bool = False):
        # Create a Basic Auth header manually (same as curl)
        credentials = f"{client_id}:{client_secret}"
        b64_credentials = base64.b64encode(credentials.encode()).decode()

        self.client_id = client_id
        self.headers = {
            "Authorization": f"Basic {b64_credentials}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        self.common_headers = {}

        if options.get('use_http_user_agent_str'):
            self.common_headers['User-Agent'] = options['use_http_user_agent_str']

        if options.get('debug') == True:
            # Set debug level to 1 to dump all HTTP traffic to stdout
            import http
            http.client.HTTPConnection.debuglevel = 1

        if not sandbox:
            self._base_url = BASE_URL
            self._api_base_url = API_BASE_URL
        else: 
            self._base_url = BASE_URL_SANDBOX
            self._api_base_url = API_BASE_URL_SANDBOX


    def isSandBox(self):
        return self._base_url == BASE_URL_SANDBOX

    def post(self, request_to: PathTo, params):
        return requests.post(
             self._base_url + request_to.getPath(),
             headers=(self.headers | self.common_headers),
             params=params
         )

    def getSessionRequestor(self, access_token:str):
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.allegro.public.v1+json",
            "Content-Type": "application/vnd.allegro.public.v1+json"
        }

        all_headers = headers | self.common_headers

        session = requests.Session()

        return (lambda path, params: session.get(self._api_base_url + path, headers=all_headers, params=params),
                lambda path, params: session.post(self._api_base_url + path, headers=all_headers, params=params),
                lambda path, params, payload: session.patch(self._api_base_url + path, headers=all_headers, params=params, json=payload))
