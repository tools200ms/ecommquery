from ecommquery.ecommquery import Mode
from ecommquery.core.validators import RegExValidator, PathValidator

from ecommquery.core.endpoint import Endpoint
from ecommquery.ext.amazon_api0sp.core.service_amsp import ServiceAmSP
from ecommquery.ext.filesystem.core.service_fs import ServiceFS


# Amazon Selling Partnr API
class EndpointFS(Endpoint):

    @staticmethod
    def reg_name():
        return 'filesystem'

    @staticmethod
    def name() -> str:
        return "File system access"

    def __init__(self, params : {}):
        super().__init__({'path': Endpoint.Constr(PathValidator)},
                        params)

    def info(self):
        info = self._path
        if self._memo != None: info += "\n\t" + self._memo

        return info

    def _getService(self, mode: Mode):
        return ServiceFS( self._path, **Mode.as_args(mode) )

Endpoint.register(EndpointFS)

