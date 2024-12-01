from ecommquery.lib.atomic.atomic import Atomic


class PSPrice (Atomic):

    def __init__(self):
        super().__init__()
        self.__price = None

    def value(self, price:float = None):
        if price == None:
            return self.__price

        if self.__price != None:
            self.markChange()

        self.__price = price

    def rawValue(self, value:str = None):
        if value == None:
            return f'{self.__price:.6f}'

        number = float(value)

        if self.__price != None:
            self.markChange()

        self.__number = number
