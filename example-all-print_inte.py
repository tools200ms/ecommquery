
from ecommquery import *
from ecommquery.core.loader_ini import IniLoader
from ecommquery.exceptions import EcommQueryError, Termination
from prestapyt import PrestaShopWebServiceError

def main():
    ret_code = 0
    try:
        inegr = Integrations()
        inegr.addLoaderAndRead(IniLoader('example-all.ini'))

        inegr.print()

    except FileNotFoundError as err:
        print(err)
        ret_code = Termination.GENERAL_ERROR
    except EcommQueryError as ecq_err:
        print(ecq_err)
        ret_code = Termination.GENERAL_ERROR
    except PrestaShopWebServiceError as psw_err:
        print(psw_err)
        ret_code = Termination.GENERAL_ERROR

    return ret_code

if __name__ == "__main__":
    main()
