import re
from abc import abstractmethod


class Validator:
    @staticmethod
    def text(str):
        try:
            str.encode('utf-8')
        except UnicodeEncodeError:
            return False

        return len(str) < 512

class ParamValidator:
    @abstractmethod
    def validate(self, name):
        pass

    def getDefaultValue(self):
        return None

    @staticmethod
    def getNone():
        return None

class ListValidator (ParamValidator):
    def __init__(self, list: [], def_idx: int = None):
        self.__list = list
        self.__def_idx = def_idx

    def validate(self, name):
        return name.strip().lower() in self.__list

    def getDefaultValue(self):
        if self.__def_idx == None:
            return None

        return self.__list[self.__def_idx]


class RegExValidator (ParamValidator):
    def __init__(self, pattern):
        self.__re = re.compile(pattern)

    def validate(self, str):
        return self.__re.match(str)

