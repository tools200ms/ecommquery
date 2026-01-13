from pprint import pprint

from ecommquery.ext.prestashop_api.lib.atomic.ps_int_numb import PSIntNumber
from ecommquery.lib.stock import Stock


class PSStock(Stock):
    def __init__(self, raw):
        super().__init__()
        self.__raw = raw

        if 'stock_available' not in raw:
            raise Exception('Inconsistent data')

        self.__raw_buf = raw['stock_available']
        self._quantity = PSIntNumber(self.__raw_buf['quantity'])

    def getRaw(self):
        return self.__raw

    @property
    def quantity(self):
        return self._quantity.value()

    @quantity.setter
    def quantity(self, value):
        self._quantity.value(value)

    def prepareToCommit(self):
        if self._quantity.hasChanged():
            self.__raw_buf['quantity'] = self._quantity.rawValue()
            pprint(self.__raw)
            return True

        return False
