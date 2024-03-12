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
            self.url = url
        else:
            raise Exception('Invalid url')

        self.key = key

        self.ps_srv = None

    def name(self):
        return "PrestaShop API"

    def info(self):
        info = self.url
        if self.memo != None: info += "\n" + self.memo

        return info

    def getService(self):
        if self.ps_srv == None:
            self.ps_srv = ServicePS( self.url, self.key, verbose=False )

        return self.ps_srv

#Endpoint.endpointtypes = {'presta_api': EndpointPS}
Endpoint.register(EndpointPS)
