import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

from ecommquery.core.service_management import ManagementService
from ecommquery.ext.web_scrap.lib.wps_product import WPSProduct


class ServiceWPScrap(ManagementService):

    def __init__(self, url, verbose=False):
        self.url = url
        self.verbose = verbose

    def getProductList(self, criteria = None):

        return None

    def getProduct(self, item_no):
        page_url = urljoin(self.url, item_no)

        response = requests.get(page_url)

        # Check if request was successful
        if response.status_code != 200:
            return False

        return WPSProduct(BeautifulSoup(response.text, 'html.parser'))
