import re

from pathlib import Path
from abc import abstractmethod

from ecommquery.exceptions import LocalResourceAccessError, CallError
from email_validator import validate_email, EmailNotValidError


class Validator:
    @staticmethod
    def text(str):
        try:
            str.encode('utf-8')
        except UnicodeEncodeError:
            return False

        return len(str) < 512

    @staticmethod
    def onelinetext(str):
        try:
            str.encode('utf-8')
        except UnicodeEncodeError:
            return False

        str = str.strip()
        if len(str.splitlines()) != 1:
            return False

        return len(str) < 512

class ParamValidator:
    @abstractmethod
    def validate(self, value: str) -> (bool, object):
        pass

    def getDefaultValue(self) -> object:
        return None

    # @staticmethod
    # def getNone():
    #     return None

class ListValidator (ParamValidator):
    def __init__(self, list: [], def_idx: int = None):
        self.__list = list
        self.__def_idx = def_idx

    def validate(self, value: str) -> (bool, object):
        val = value.strip().lower()
        if val in self.__list:
            return True, val
        return False, None

    def getDefaultValue(self):
        if self.__def_idx == None:
            return None

        return self.__list[self.__def_idx]

class LoginNameValidator:

    MAX_LOGIN_NAME_LENGTH = 64

    def __init__(self, obligatory_letter_first: bool = True, also_accept_email: bool = False):
        if obligatory_letter_first:
            self._base_validation = self._first_must_be_aletter
        else:
            self._base_validation = self._there_must_be_aletter

        self._accept_email = also_accept_email

    def validate(self, name: str) -> (bool, object):
        name = name.strip()
        if len(name) > LoginNameValidator.MAX_LOGIN_NAME_LENGTH:
            return False, None

        res, name = self._base_validation(name.lower())

        if self._accept_email:
            try:
                email_info = validate_email(name, check_deliverability=True)
                name = email_info.deliverable_address
                res = True
            except EmailNotValidError as e:
                return False, None

        return res, name

    @staticmethod
    def _first_must_be_aletter(name: str):
        return re.fullmatch(r'^[a-z][a-z0-9_.-]*$', name) != None, name

    @staticmethod
    def _there_must_be_aletter(name: str):
        return name.isdigit() == False and re.fullmatch(r'^[a-z0-9_.-]*$', name) != None, name


class RegExValidator (ParamValidator):
    def __init__(self, pattern):
        self.__re = re.compile(pattern)

    def validate(self, value: str) -> (bool, object):
        if self.__re.match(value):
            return True, value
        return False, None

class GenericKeyValidator (RegExValidator):
    def __init__(self):
        super().__init__('[A-Za-z0-9|\\-|\\.]{16,512}')

class YesNoValidator (ParamValidator):

    def __init__(self, default: bool):
        self.__def_val = default

    # def normValue(self):
    #     if self.__val == None:
    #         raise CallError('Value not set')
    #
    #     return self.__val

    def validate(self, value: str) -> (bool, object):
        if value.lower() in {"y", "yes", "true", "1", "on"}:
            return True, True
        elif value.lower() in {"n", "no", "false", "0", "non"}:
            return True, False

        return False, None


    def getDefaultValue(self):
        return self.__def_val

# TODO: add options:
# IF_DIR_EXISTS, IF_FILE_EXISTS
# CREATE_IF_MISSING_DIR, CREATE_IF_MISSING_FILE
class PathValidator(ParamValidator):
    def __init__(self, def_path: str):
        if not self.validate(def_path):
            raise CallError( f"Illegal path name: {def_path}" )

        self.__def_path = def_path

    def validate(self, path: str) -> bool:
        try:
            Path(path).resolve()
        except (OSError, RuntimeError):
            return False, path

        return len(path) < 1024, path

    def getDefaultValue(self):
        return self.__def_path

