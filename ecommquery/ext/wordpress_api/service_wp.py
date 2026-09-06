import logging
from urllib.parse import urljoin

import requests
from requests.auth import HTTPBasicAuth

from ecommquery.core.service_management import ManagementService
from ecommquery.lib.error import ExternalServiceError

# LOGGER

# Enable HTTP client debug logging
import http.client

http.client.HTTPConnection.debuglevel = 1

# Configure logging format
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

# END OF LOGGER


class DummySession:
    def query(self, *args, **kwargs):
        raise RuntimeError("Pretend mode ON")

    def close(self):
        pass

class ServiceWP(ManagementService):

    def __init__(self, api_url, login, app_pass, verbose: bool, debug: bool, pretend: bool):
        #super().__init__(debug = debug, session = session, verbose = verbose)

        if not pretend:
            session = requests.Session()
            session.auth = HTTPBasicAuth(login, app_pass)
            session.headers.update({"Content-Type": "application/json"})
            session.get("http://localhost:8080/wp-json/wp/v2/settings/")
        else:
            session = DummySession

        self._pretend = pretend
        self._session = session
        self._baseurl = api_url.rstrip('/') + '/'
        self._timeout = 30

    def query(self, path: str, params = None):
        full_url = urljoin(self._baseurl, path.lstrip('/'))

        response = self._session.get(full_url) #, params = params, timeout = self._timeout)
        response.raise_for_status()

        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            print(response.text)
            raise ExternalServiceError()

    def test(self):
        resp = self.query("settings")
        print(resp)

    def close(self):
        self._session.close()

