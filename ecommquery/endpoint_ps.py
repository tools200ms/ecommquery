from prestapyt import PrestaShopWebServiceDict

from ecommquery.endpoint import Endpoint

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

    def name(self):
        return "PrestaShop"

    def info(self):
        info = self.url
        if self.memo != None: info += "\n" + self.memo

        return info

    def getService(self):
        return PrestaShopWebServiceDict( self.url, self.key, verbose=False )

#Endpoint.endpointtypes = {'presta_api': EndpointPS}
Endpoint.register('presta_api', EndpointPS)
