from ecommquery.ext.allegro_api.core.requestor import Requestor
from datetime import datetime, timedelta


class Session:
    def __init__(self,
                 access_token,
                 refresh_token,
                 expires: str|datetime,
                 scope = None, allegro_api = None, iss = None, jti = None, token_type = None):
        self._access_token = access_token
        self._allegro_api = allegro_api
        if type(expires) == str:
            self._expires_on = Session.getExpireOn(int(expires))
        elif type(expires) == datetime:
            self._expires_on = expires

        self._refresh_token = refresh_token

        # Extra details: 
        self._iss = iss
        self._jti = jti
        self._scope = scope
        self._token_type = token_type

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

    @staticmethod
    def getExpireOn(expires_in: int):
        return (datetime.now() + timedelta(seconds=expires_in - 5))

    def request(self):
        pass
    
    def refresh(self):
        pass
