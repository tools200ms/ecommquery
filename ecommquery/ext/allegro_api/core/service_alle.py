import json
import pprint
import urllib
from base64 import b64encode

import urllib3

from ecommquery.core.service_management import ManagementService
from ecommquery.ext.amazon_api0sp.core import amsp_constants

class ServiceAlle(ManagementService):

    def __init__(self, client_id:str, client_secret:str, sandbox: bool, verbose: bool, debug: bool, pretend: bool):
        pass

