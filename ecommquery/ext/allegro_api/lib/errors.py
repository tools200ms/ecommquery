from ecommquery.lib.error import ServiceConnactionError


class AllegroConnectionError(ServiceConnactionError):
    pass

class AllegroConnectionTimeOutUserAuthorizationError(AllegroConnectionError):
    pass
