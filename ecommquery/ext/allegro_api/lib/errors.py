from ecommquery.lib.error import NetworkConnectionError, UserMissAction


class AllegroConnectionError(NetworkConnectionError):
    pass

class AllegroConnectionTimeOutUserAuthorizationError(UserMissAction):
    pass
