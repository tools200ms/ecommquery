from ecommquery.ecommquery import Mode
from ecommquery.core.validators import RegExValidator

from ecommquery.core.endpoint import Endpoint
from ecommquery.ext.amazon_api0sp.core.service_amsp import ServiceAmSP


# Amazon Selling Partnr API
class EndpointAmSP(Endpoint):

    @staticmethod
    def reg_name():
        return 'amazon_sp_api'

    @staticmethod
    def name():
        return "Amazon Selling Partner (SP) API"

    def __init__(self, params : {}):
        # This should validate Amazon Client ID and secret key
        am_validator = RegExValidator('[a-z0-9|\.|\-]{16,96}')
        rt_validator = RegExValidator('[a-zA-Z0-9|_|\-|\|]{128,512}')

        super().__init__({'client_id': Endpoint.Constr('_client_id', am_validator),
                          'client_secret_key': Endpoint.Constr('_client_secret_key', am_validator),
                          'refresh_token': Endpoint.Constr('_refresh_token', rt_validator)},
                        params)

    def info(self):
        info = self._client_id
        if self._memo != None: info += "\n" + self._memo

        return info

    def _getService(self, mode: Mode):
        return ServiceAmSP( self._client_id, self._client_secret_key, **Mode.as_args(mode) )

Endpoint.register(EndpointAmSP)

