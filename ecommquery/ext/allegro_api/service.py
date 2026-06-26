'''
Based on:
https://developer.allegro.pl/tutorials/uwierzytelnianie-i-autoryzacja-zlq9e75GdIR
'''
from json import JSONDecodeError

from requests import HTTPError

from ecommquery import Endpoint
from ecommquery.core.service_management import ManagementService
from ecommquery.core.stash import Stash

from ecommquery.ext.allegro_api.core.authenticator import Authenticator
from ecommquery.ext.allegro_api.core.requestor import Requestor
from ecommquery.ext.allegro_api.core.session import Session
from ecommquery.ext.allegro_api.lib.errors import AllegroConnectionError


class ServiceAlle(ManagementService):

    def __init__(self, client_id:str, client_secret:str, options:{}, sandbox: bool, verbose: bool, debug: bool, pretend: bool):
        if debug == True:
            options['debug'] = debug

        self._req = Requestor(client_id, client_secret, options, sandbox)

        module = Endpoint.getEpName(self.__class__)

        self._stash = Stash(module, self.id())

        #try:
        self._stash.load(recreate_if_broken=True)
        #except JSONDecodeError as json_err:
        #    raise Exception(f"Failed to load stash file. Please check the file format and try again:\n    {json_err}")

    def id(self) -> str:
        if self._req.isSandBox():
            return self._req.client_id + "-sandbox"

        return self._req.client_id

    class Pending:
        def __init__(self, waiting_fun, autn:Authenticator):
            self._waiting_fun = waiting_fun
            self._autn = autn

        def waitForSession(self):
            return self._waiting_fun()

        def getDeviceCode(self):
            return self._autn.device_code

        def getUserCode(self):
            return self._auth.user_code

        def getVerificationUri(self):
            return self._auth.verification_uri

        def getVerificationUriComplete(self):
            return self._autn.verification_uri_complete

        def getExpiresIn(self):
            return self._autn.expires_in

    def _establish(self, reset:bool = False) -> Session:
        access_token = self._stash.get("access_token")
        refresh_token = self._stash.get("refresh_token")
        expires_on = self._stash.getDate("expires_on")

        if access_token == None or reset:
            auth = Authenticator.start_device_flow(self._req)

            auth.printMessage()
            auth.printDetails()

            def wait_for_user_authentification():
                session = auth.poll_for_token(self._req)

                self._stash.set("access_token", session.access_token)
                self._stash.set("refresh_token", session.refresh_token)
                self._stash.setDate("expires_on", session.expires_on)
                self._stash.save()
                return session

            return ServiceAlle.Pending(wait_for_user_authentification, auth)

        session = Session(self._req, access_token, refresh_token, expires_on)
        if not session.isFresh():
            if session.isStale():
                self.refresh(session)
            else:
                print("Session is stale, trying to connect anyway.")
                self.refresh(session)

            # session is fresh, let's use it

        # operations on session
        #print(auth)
        return session

    def establish(self) -> Session:
        try:
            session = self._establish()
        except HTTPError as err:
            try:
                session = self._establish(reset=True)
            except HTTPError as err:
                raise AllegroConnectionError() from err

        return session

    def refresh(self, session: Session) -> Session:
        session.refreshAccessToken()
        self._stash.set("access_token", session.access_token)
        self._stash.set("refresh_token", session.refresh_token)
        self._stash.setDate("expires_on", session.expires_on)
        self._stash.save()

    def clear(self):
        # clear stash ...
        ...

    def close(self):
        pass
