'''
Based on:
https://developer.allegro.pl/tutorials/uwierzytelnianie-i-autoryzacja-zlq9e75GdIR
'''
from datetime import datetime

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

        self._stash = Stash(module, id())
        self._stash.load()

    def id(self) -> str:
        if self._req.isSandBox():
            return self._req.client_id + "-sandbox"

        return self._req.client_id

    def establish(self):
        access_token = self._stash.get("access_token")
        if access_token == None:
            auth = Authenticator.start_device_flow(self._req)
            auth.printMessage()
            auth.printDetails()
            session = auth.poll_for_token(self._req)

            self._stash.set("access_token", session.access_token)
            self._stash.set("refresh_token", session.refresh_token)
            self._stash.set("expires_on", session.expires_on.strftime('%Y-%m-%d %H:%M:%S'))
        else:
            session = Session(self._stash.get("access_token"),
                              self._stash.get("refresh_token"),
                              datetime.strptime(self._stash.get("expires_on"), '%Y-%m-%d %H:%M:%S')
                              )

        # operations on session
        print(auth)
