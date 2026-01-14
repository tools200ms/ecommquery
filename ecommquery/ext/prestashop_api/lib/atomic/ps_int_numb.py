from ecommquery.lib.atomic.atomic import Atomic


class PSIntNumber (Atomic):

    # TODO: add declaration if negative number can be provided
    def __init__(self, raw_value):
        super().__init__()
        self.__number = self.__class__._getValue(raw_value)

    def __str__(self):
        return str(self.__number)

    @staticmethod
    def _getValue(value: str) -> int:
        if not value.lstrip('-').isdigit():
            raise Exception(f'Expected numeric value, got {value}')

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
            return str(self)

        number = PSIntNumber._getValue(raw_value)

        if self.__number != number:
            self.markChange()
            self.__number = number

        return None
