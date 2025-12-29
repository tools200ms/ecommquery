'''
Based on:
https://developer.allegro.pl/tutorials/uwierzytelnianie-i-autoryzacja-zlq9e75GdIR
'''
from datetime import datetime
from json import JSONDecodeError

from ecommquery import Endpoint
from ecommquery.core.service_management import ManagementService
from ecommquery.core.stash import Stash

from ecommquery.ext.allegro_api.core.authenticator import Authenticator
from ecommquery.ext.allegro_api.core.requestor import Requestor
from ecommquery.ext.allegro_api.core.session import Session


class ServiceAlle(ManagementService):

    def __init__(self, client_id:str, client_secret:str, sandbox: bool, verbose: bool, debug: bool, pretend: bool):
        self._req = Requestor(client_id, client_secret, sandbox)

        module = Endpoint.getEpName(self.__class__)

        self._stash = Stash(module, self.id())

        try:
            self._stash.load()
        except JSONDecodeError as json_err:
            raise Exception(f"Failed to load stash file. Please check the file format and try again:\n    {json_err}")

    def id(self) -> str:
        if self._req.isSandBox():
            return self._req.client_id + "-sandbox"

        return self._req.client_id

    def establish(self):
        access_token = self._stash.get("access_token")
        refresh_token = self._stash.get("refresh_token")
        expires_on = self._stash.getDate("expires_on")

        if access_token == None:
            auth = Authenticator.start_device_flow(self._req)
            auth.printMessage()
            auth.printDetails()
            session = auth.poll_for_token(self._req)

            self._stash.set("access_token", session.access_token)
            self._stash.set("refresh_token", session.refresh_token)
            self._stash.setDate("expires_on", session.expires_on)
            self._stash.save()
        else:
            session = Session(self._req, access_token, refresh_token, expires_on)
            if not session.isFresh():
                if session.isStale():
                    self.refresh(session)
                else:
                    print("Session is invalid.")
                    return None
            # session is fresh, let's use it

        # operations on session
        #print(auth)
        return session

    def refresh(self, session: Session) -> Session:
        session.refreshAccessToken()
        self._stash.set("access_token", session.access_token)
        self._stash.set("refresh_token", session.refresh_token)
        self._stash.setDate("expires_on", session.expires_on)
        self._stash.save()

    def close(self):
        pass
