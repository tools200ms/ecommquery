import validators

from ecommquery.core.validators import RegExValidator, LoginNameValidator
from ecommquery.ecommquery import Mode

from ecommquery.core.endpoint import Endpoint
from ecommquery.ext.wordpress_api.service_wp import ServiceWP


class EndpointWP(Endpoint):

    @staticmethod
    def reg_name():
        return 'wp_api'

    @staticmethod
    def name():
        return "WordPress API"

    def __init__(self, params : {}, id:str):
        super().__init__({'url': Endpoint.Constr(validators.url, obligatory = True),
                          'login': Endpoint.Constr(LoginNameValidator(also_accept_email = True).validate, obligatory = True),
                          'app_password': Endpoint.Constr(
                            # Validate if string looks "like" a key.
                            # Exact validation is made by library that
                            # talks to API.
                            # This is "first" step generic validation.
                            RegExValidator('[a-zA-Z0-9|-|_]{16,96}'), True, 'apppass', True)},
                        params, id )

    def info(self):
        info = self._url
        if self._memo != None: info += "\n\t" + self._memo

        return info

    def _getService( self, mode: Mode ):

        api_url = f"{self._url.rstrip('/')}/wp-json/wp/v2"

        return ServiceWP( api_url, self._login, self.__apppass, **Mode.as_args(mode) )

Endpoint.register( EndpointWP )
