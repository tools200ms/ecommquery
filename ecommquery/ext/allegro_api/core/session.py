import requests

from ecommquery.ext.allegro_api.core.requestor import Requestor
from datetime import datetime, timedelta

from ecommquery.ext.allegro_api.lib.constants import BASE_URL_SANDBOX


class Session:
    def __init__(self,
                 access_token,
                 refresh_token,
                 expires_in: int|datetime,
                 scope = None, allegro_api = None, iss = None, jti = None, token_type = None):
        self._access_token = access_token
        self._allegro_api = allegro_api
        if type(expires_in) == int:
            if expires_in <= 0:
                raise ValueError("Invalid expires_in value")
            self._expires_on = Session.__getExpireOn(expires_in)
        elif type(expires_in) == datetime:
            self._expires_on = expires_in
        else:
            self._expires_on = None

        self._refresh_token = refresh_token

        # Extra details: 
        self._iss = iss
        self._jti = jti
        self._scope = scope
        self._token_type = token_type

    @staticmethod
    def __getExpireOn(expires_in: int):
        return (datetime.now() + timedelta(seconds=expires_in - 1))
    
    @property
    def access_token(self):
        return self._access_token

    @property
    def allegro_api(self):
        return self._allegro_api

    @property
    def expires_on(self):
        return self._expires_on

    @property
    def refresh_token(self):
        return self._refresh_token


    @property
    def token_type(self):
        return self._token_type

    def ACValidForSec(self):
        return int((self._expires_on - datetime.now()).total_seconds())
