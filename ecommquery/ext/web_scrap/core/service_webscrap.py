import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

from ecommquery.core.service_management import ManagementService
from ecommquery.ext.web_scrap.lib.web_product import WEBProduct


class ServiceWebScrap(ManagementService):

    def __init__(self, url, verbose: bool, debug: bool, pretend: bool):
        self.__verbose = verbose
        self.__debug = debug
        self.__pretend = pretend

        self.url = url

    def getProductList(self, criteria = None):

        return None

    def getProduct(self, item_no):
        page_url = urljoin(self.url, item_no)

        response = requests.get(page_url)

        # Check if request was successful
        if response.status_code != 200:
            return False

        return WEBProduct(BeautifulSoup(response.text, 'html.parser'))
