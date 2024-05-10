

# Failure while acquiring data
class EcommQueryError (Exception):
    pass

# Illegal or misspelled syntax
class SyntaxError(Exception):
    pass

# Incorrect data format
class DataformatError(Exception):
    pass

# Error while accessing local or internet (external) resource
class LocalResourceAccessError(Exception):
    pass

class ExternalResourceAccessError(Exception):
    pass

# Internal application error
class CallError(Exception):
    pass
