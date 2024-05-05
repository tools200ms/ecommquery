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

    def __init__(self, params : {}):
        super().__init__({'url': Endpoint.Constr('_url', validators.url),
                          'api_secret_key': Endpoint.Constr('_key',
                            # don't do to strict validation, if API provider would
                            # decide to support longer keys, or extend it by a low casec haracter cases
                            # characters (assuming that UPPER case characters are curently used)
                            # this code sould handle change without updates.
                            # Exact validation is made by library that talks to API
                            RegExValidator('[a-zA-Z0-9|\-|\_]{16,96}'))},
                        params)

    def info(self):
        info = self._url
        if self._memo != None: info += "\n" + self._memo

        return info

    def _getService(self, mode: Mode):
        return ServicePS( self._url, self._key, **Mode.as_args(mode) )

Endpoint.register(EndpointPS)
