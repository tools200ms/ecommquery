import validators

from ecommquery import Endpoint
from ecommquery.core.validators import RegExValidator
from ecommquery.ecommquery import Mode
from ecommquery.ext.web_scrap.core.servicescrap_web import ServiceWEBScrap


class EndpointScrapWEB(Endpoint):

    @staticmethod
    def reg_name():
        return 'web_scrap'

    def __init__(self, params : {}):
        super().__init__({'url': Endpoint.Constr( '_url', validators.url )},
                         params)

    @staticmethod
    def name():
        return "WordPress - scrapping"

    def info(self):
        return self._url

    def _getService(self, mode: Mode):
        return ServiceWEBScrap(self._url, **Mode.as_args(mode))

Endpoint.register(EndpointScrapWEB)
