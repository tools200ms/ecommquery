import re
from unidecode import unidecode


class URLFun:

    @staticmethod
    def key_friendly_str(s:str):
        s = re.sub(r'[^a-z0-9]', '-', unidecode(s).lower())

        return s
