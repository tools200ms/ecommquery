import re


class Validator:
    @staticmethod
    def text(str):
        try:
            str.encode('utf-8')
        except UnicodeEncodeError:
            return False

        return len(str) < 512

class RegExValidator:
    def __init__(self, pattern):
        self.__re = re.compile(pattern)

    def validator(self, str):
        return self.__re.match(str)

