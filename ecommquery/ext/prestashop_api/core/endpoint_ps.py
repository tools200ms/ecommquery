import validators

from ecommquery.ext.prestashop_api.core.service_ps import ServicePS

from ecommquery.core.endpoint import Endpoint

class EndpointPS(Endpoint):

    @staticmethod
    def reg_name():
        return 'presta_api'

    def __init__(self, params : {}):
        super().__init__({'url': Endpoint.Constr('_url', None),
                          'api_secret_key': Endpoint.Constr('_key', None)},
                        params)

    @staticmethod
    def name():
        return "PrestaShop API"

    def info(self):
        info = self._url
        if self._memo != None: info += "\n" + self._memo

        return info

    def _getService(self):
        return ServicePS( self._url, self._key, verbose = False )

#Endpoint.endpointtypes = {'presta_api': EndpointPS}
Endpoint.register(EndpointPS)
