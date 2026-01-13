from ecommquery.lib.atomic.atomic import Atomic


class PSFixPointNumber (Atomic):

    def __init__(self, raw_value):
        super().__init__()
        self.__number = PSFixPointNumber._getValue(raw_value)

    def __str__(self):
        return f'{self.__number[0]}.{self.__number[1]:06d}'

    def value(self, number:(int,int) = None):
        if number == None:
            return self.__number

        if self.__number != number:
            self.markChange()

        self.__number = number

    @staticmethod
    def _getValue(value:str)->(int,int):
        val_arr = value.split('.')

        if len(val_arr) != 2:
            raise ValueError("Not a fixed point number")

        if not val_arr[0].lstrip('-').isdigit():
            raise ValueError("Not an integer number")

        if not val_arr[1].isdigit() or len(val_arr[1]) != 6:
            raise ValueError("Wrong number format")

        return (int(val_arr[0]),int(val_arr[1]))

    def rawValue(self, value: str = None) -> str | None:
        if value == None:
            return str(self)

        number = PSFixPointNumber._getValue(value)

        if self.__number != number:
            self.markChange()
            self.__number = number

        return None
