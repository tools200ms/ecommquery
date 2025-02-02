
from pprint import pprint

from ecommquery import *
from ecommquery.core.loader_ini import IniLoader
from ecommquery.exceptions import EcommQueryError, Termination
from prestapyt import PrestaShopWebServiceError

# TODO: <annotation>

def main():
    ret_code = 0
    try:
        integr = Integrations(mode = Mode.WORK)
        integr.addLoaderAndRead(IniLoader('example-fs.ini'))

        integr.print()
        gpt = integr.getService(endpoint="chatgpt")
        fss = integr.getService(endpoint='filesystem')
        file = fss.get_file("docs.py")

        res = gpt.sendPrompt('report_py_code_summary', [file])

        print("============\n" + res + "============\n")
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
