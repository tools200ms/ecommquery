
# User did, or did not do something tha was expected (requied?) to do
# e.g.: User did not authorized a certain action, so it has to be abounded
class UserMissAction(Exception):
    pass

# Something has happen on the network - not our fault.
class NetworkConnectionError(Exception):
    pass

class ExternalServiceError(Exception):
    pass
