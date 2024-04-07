import validators

from ecommquery import Endpoint
from ecommquery.ext.wordpress_scrap.core.servicescrap_wp import ServiceWPScrap


class EndpointScrapWP(Endpoint):

    @staticmethod
    def reg_name():
        return 'wp_scrap'

    def __init__(self, params : {}):
        super().__init__({'url': Endpoint.Constr('_url', validators.url)},
                         params)

    @staticmethod
    def name():
        return "WordPress - scrapping"

    def info(self):
        return self._url

    def _getService(self):
        return ServiceWPScrap(self._url, verbose=False)

Endpoint.register(EndpointScrapWP)
