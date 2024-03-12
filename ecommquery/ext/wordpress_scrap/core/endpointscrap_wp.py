import validators

from ecommquery import Endpoint
from ecommquery.ext.wordpress_scrap.core.servicescrap_wp import ServiceWPScrap


class EndpointScrapWP(Endpoint):

    @staticmethod
    def reg_name():
        return 'wp_scrap'

    @staticmethod
    def factory(params):
        if 'memo' in params:
            memo = params['param']
        else:
            memo = None

        return EndpointScrapWP(params['url'], memo)

    def __init__(self, url, memo):
        super().__init__(memo)

        if validators.url(url):
            self.url = url
        else:
            raise Exception('Invalid url')

        self.__srv = None

    def name(self):
        return "WordPress - scrapping"

    def info(self):
        return self.url

    def getService(self):
        if self.__srv == None:
            self.__srv = ServiceWPScrap( self.url, verbose=False )

        return self.__srv

Endpoint.register(EndpointScrapWP)
