from ecommquery.lib.atomic.atomic import Atomic


class PSIntNumber (Atomic):

    def __init__(self, raw_value):
        super().__init__()
        self.__number = PSIntNumber._getValue(raw_value)

    @staticmethod
    def _getValue(value: str) -> int:
        return int(value)

    def value(self, number:int = None)->int|None:
        if number == None:
            return self.__number

        if self.__number != number:
            self.markChange()
            self.__number = number

        return None

    def rawValue(self, raw_value: str = None) -> str | None:
        if raw_value == None:
            return str(self.__number)

        number = PSIntNumber._getValue(raw_value)

        if self.__number != number:
            self.markChange()
            self.__number = number

        return None
