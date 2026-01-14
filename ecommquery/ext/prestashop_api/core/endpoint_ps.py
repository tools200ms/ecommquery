import validators

from ecommquery.core.validators import RegExValidator
from ecommquery.ecommquery import Mode
from ecommquery.ext.prestashop_api.core.service_ps import ServicePS

from ecommquery.core.endpoint import Endpoint

class EndpointPS(Endpoint):

    @staticmethod
    def reg_name():
        return 'presta_api'

    @staticmethod
    def name():
        return "PrestaShop API"

    def __init__(self, params : {}, id:str):
        super().__init__({'url': Endpoint.Constr(validators.url),
                          'api_secret_key': Endpoint.Constr(
                            # Validate if string looks "like" a key.
                            # Exact validation is made by library that
                            # talks to API.
                            # This is "first" step generic validation.
                            RegExValidator('[a-zA-Z0-9|-|_]{16,96}'), True, 'key', True)},
                        params, id )

    def info(self):
        info = self._url
        if self._memo != None: info += "\n\t" + self._memo

        return info

    def _getService( self, mode: Mode ):
        return ServicePS( self._url, self.__key, **Mode.as_args(mode) )

Endpoint.register( EndpointPS )
