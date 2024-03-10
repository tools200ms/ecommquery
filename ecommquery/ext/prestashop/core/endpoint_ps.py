from ecommquery.ext.prestashop.core.service_ps import PSService

from ecommquery.core.endpoint import Endpoint

class EndpointPS(Endpoint):

    @staticmethod
    def factory(params):
        if 'memo' in params:
            memo = params['param']
        else:
            memo = None

        return EndpointPS( params['url'], params['api_secret_key'], memo )

    def __init__(self, url, key, memo = None):
        super().__init__( memo )
        self.url = url
        self.key = key

        self.ps_srv = None

    def name(self):
        return "PrestaShop"

    def info(self):
        info = self.url
        if self.memo != None: info += "\n" + self.memo

        return info

    def getService(self):
        if self.ps_srv == None:
            self.ps_srv = PSService( self.url, self.key, verbose=False )

        return self.ps_srv

#Endpoint.endpointtypes = {'presta_api': EndpointPS}
Endpoint.register('presta_api', EndpointPS)
