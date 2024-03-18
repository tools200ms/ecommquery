from ecommquery.lib.atomic.atomic import Atomic


class PSNumber (Atomic):

    def __init__(self):
        super().__init__()
        self.__number = None

    def value(self, number:float = None):
        if number == None:
            return self.__number

        if self.__number != None:
            self.markChange()

        self.__number = number

    def rawValue(self, value:str = None):
        if value == None:
            return f'{self.__number:.6f}'

        number = float(value)

        if self.__number != None:
            self.markChange()

        self.__number = number
