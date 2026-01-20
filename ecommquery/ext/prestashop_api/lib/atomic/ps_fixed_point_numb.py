from ecommquery.lib.atomic.atomic import Atomic


class PSFixPointNumber (Atomic):

    def __init__(self, raw_value, precision = 6):
        super().__init__()
        self.__number = self.__class__._getValue(raw_value, precision)
        self._precision = precision
        self._multiplier = 10**precision

    def __str__(self):
        format = f"0{self._precision}d"
        return f'{self.__number[0]}.{self.__number[1]:{format}}'

    def value(self, number:int = None):
        if number == None:
            return self.__number[0] * self._multiplier + self.__number[1]

        if self.__number != number:
            self.markChange()

        self.__number = (int(number / self._multiplier), number % self._multiplier)

    @classmethod
    def _getValue(cls, value:str, precision)->(int,int):
        val_arr = value.split('.')

        if len(val_arr) != 2:
            raise ValueError("Not a fixed point number")

        if not val_arr[0].lstrip('-').isdigit():
            raise ValueError("Not an integer number")

        if not val_arr[1].isdigit() or len(val_arr[1]) != precision:
            raise ValueError("Wrong number format")

        return (int(val_arr[0]),int(val_arr[1]))

    def rawValue(self, value: str = None) -> str | None:
        if value == None:
            return str(self)

        number = self._getValue(value, self._precision)

        if self.__number != number:
            self.markChange()
            self.__number = number

        return None
