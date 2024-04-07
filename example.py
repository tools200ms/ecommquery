
from ecommquery import *
from ecommquery.core.loader_ini import IniLoader
from ecommquery.exceptions import EcommQueryError
from prestapyt import PrestaShopWebServiceError

try:
    inegr = Integrations()
    inegr.addLoaderAndRead( IniLoader('example.ini') )

    inegr.print()

except FileNotFoundError as err:
    print(err)
except EcommQueryError as ecq_err:
    print(ecq_err)
except PrestaShopWebServiceError as psw_err:
    print(psw_err)

