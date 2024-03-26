import validators

from ecommquery.ext.prestashop_api.core.service_ps import ServicePS

from ecommquery.core.endpoint import Endpoint

class EndpointPS(Endpoint):

    @staticmethod
    def reg_name():
        return 'presta_api'

    @staticmethod
    def factory(params):
        if 'memo' in params:
            memo = params['param']
        else:
            memo = None

        return EndpointPS( params['url'], params['api_secret_key'], memo )

    def __init__(self, url, key, memo = None):
        super().__init__( memo )

        if validators.url( url ):
            self._url = url
        else:
            raise Exception('Invalid url')

        self.__key = key

        self._ps_srv = None

    def name(self):
        return "PrestaShop API"

    def match(self, pattern: str) -> bool:
        if self._memo != None:
            if self._memo.find(pattern) != -1:
                return True

        return self._url.find(pattern) != -1

    def info(self):
        info = self._url
        if self._memo != None: info += "\n" + self._memo

        return info

    def getService(self):
        if self._ps_srv == None:
            self._ps_srv = ServicePS( self._url, self.__key, verbose = False )

        return self._ps_srv

#Endpoint.endpointtypes = {'presta_api': EndpointPS}
Endpoint.register(EndpointPS)
