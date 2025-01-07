from typing import Final

class Termination:

    GENERAL_ERROR: Final[int] = 1
    WRONG_CMD_OR_ARG: Final = 2
    def get_exit_code(self)->int:
        return 2

# Failure while acquiring data
class EcommQueryError (Exception):
    pass

# Illegal or misspelled syntax
class SyntaxError(Exception, Termination):
    pass

# Incorrect data format
class DataformatError(Exception, Termination):
    pass

# Error while accessing local or internet (external) resource
class LocalResourceAccessError(Exception, Termination):
    pass

class ExternalResourceAccessError(Exception):
    pass

# Internal application error
class CallError(Exception, Termination):
    pass
