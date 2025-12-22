import re

from pathlib import Path
from abc import abstractmethod

from ecommquery.exceptions import LocalResourceAccessError, CallError


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
    def validate(self, value: str) -> bool:
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

    def validate(self, value: str) -> bool:
        return value.strip().lower() in self.__list

    def getDefaultValue(self):
        if self.__def_idx == None:
            return None

        return self.__list[self.__def_idx]


class RegExValidator (ParamValidator):
    def __init__(self, pattern):
        self.__re = re.compile( pattern )

    def validate(self, value: str) -> bool:
        return self.__re.match(value)

class GenericKeyValidator (RegExValidator):
    def __init__(self):
        super().__init__('[a-z0-9|\.|\-]{16,512}')

class YesNoValidator (ParamValidator):

    def __init__(self, default: bool = False):
        self.__def_val = default
        self.__val = None

    def normValue(self):
        if self.__val == None:
            raise CallError('Value not set')

        return self.__val

    def validate(self, value: str) -> bool:
        if value.lower() in {"y", "yes", "true", "1", "on"}:
            self.__val = True
        elif value.lower() in {"n", "no", "false", "0", "non"}:
            self.__val = False
        else:
            return False

        return True

    def getDefaultValue(self):
        return self.__def_val

class PathValidator(ParamValidator):
    def __init__(self, def_path: str):
        if not self.validate(def_path):
            raise CallError( f"Illegal path name: {def_path}" )

        self.__def_path = def_path

    def validate(self, path: str) -> bool:
        try:
            Path(path).resolve()
        except (OSError, RuntimeError):
            return False

        return len(path) < 1024

    def getDefaultValue(self):
        return self.__def_path

