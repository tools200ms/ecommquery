
from ecommquery.ecommquery import Mode
from ecommquery.core.validators import YesNoValidator, GenericKeyValidator

from ecommquery.core.endpoint import Endpoint
from ecommquery.ext.allegro_api.service import ServiceAlle

# Amazon Selling Partnr API
class EndpointAlle(Endpoint):

    @staticmethod
    def reg_name():
        return 'allegro_api'

    @staticmethod
    def name():
        return "Allegro API"

    def __init__(self, params : {}, id:str):

        super().__init__({'client_id': Endpoint.Constr(GenericKeyValidator),
                          'client_secret': Endpoint.Constr(GenericKeyValidator),
                          'sandbox': Endpoint.Constr(YesNoValidator(False), False)},
                        params, id)

    def info(self):
        info = self._client_id
        if self._memo != None: info += "\n" + self._memo

        return info

    def _getService(self, mode: Mode):
        return ServiceAlle(self._client_id, self._client_secret, self._sandbox, **Mode.as_args(mode))

Endpoint.register(EndpointAlle, ServiceAlle)

