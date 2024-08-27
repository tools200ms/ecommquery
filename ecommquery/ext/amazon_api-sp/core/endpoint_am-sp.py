# ...
from ecommquery import RegExValidator
from ecommquery.core.endpoint import Endpoint


# Amazon Selling Partnr API
class EndpointAmSP(Endpoint):

    @staticmethod
    def reg_name():
        return 'amazon_sp_api'

    @staticmethod
    def name():
        return "Amazon Selling Partner (SP) API"

    def __init__(self, params : {}):
        super().__init__({'client_id': Endpoint.Constr('_url', validators.url),
                          'client_secret_key': Endpoint.Constr('_key',
                            # don't do to strict validation, if API provider would
                            # decide to support longer keys, or extend it by a low casec haracter cases
                            # characters (assuming that UPPER case characters are curently used)
                            # this code sould handle change without updates.
                            # Exact validation is made by library that talks to API
                            RegExValidator('[a-zA-Z0-9|\-|\_]{16,96}'))},
                        params)

    def info(self):
        info = self._url
        if self._memo != None: info += "\n" + self._memo

        return info

    def _getService(self, mode: Mode):
        return ServicePS( self._url, self._key, **Mode.as_args(mode) )

Endpoint.register(EndpointPS)

