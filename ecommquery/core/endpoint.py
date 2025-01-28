from typing import Callable

from abc import abstractmethod

from ecommquery.core.validators import Validator, ParamValidator
from ecommquery.ecommquery import Mode
from ecommquery.exceptions import DataformatError, CallError


class Endpoint:
    class Constr:
        _re_name = None
        def __init__( self, validator: Validator | Callable[[str], bool], obligatory: bool = True, re_name: str = None ):

            if isinstance( validator, ParamValidator ):
                self.validate = validator.validate
                self.getDefaultValue = validator.getDefaultValue
            else:
                self.validate = validator
                self.getDefaultValue = ParamValidator.getNone


            self.__obligatory = obligatory
            self._re_name = re_name

        def getVarName(self, name: str):
            if self._re_name is None:
                return '_' + name

            return '_' + self._re_name

        def isObligatory(self):
            return self.__obligatory

    __endpointtypes = {}
    _id = 0

    @staticmethod
    def register( ep_class ):
        Endpoint.__endpointtypes[ep_class.reg_name()] = ep_class;

    @staticmethod
    def getClass( type ):
        #global endpointtypes
        if not type in Endpoint.__endpointtypes:
            raise Exception('Endpoint of \'' + type + '\' has not been defined')

        return Endpoint.__endpointtypes[type]

    @staticmethod
    @abstractmethod
    def reg_name() -> str:
        pass

    @staticmethod
    @abstractmethod
    def name() -> str:
        pass

    def __init__( self, attr_list : {}, params : {} ):
        comm_attr_list = {'memo': Endpoint.Constr(Validator.text, False)}

        all_attr_list = comm_attr_list | attr_list

        used = {}

        for name, value in params.items():
            if name not in all_attr_list:
                raise DataformatError(f"Parameter {name} not supported, endpoint: {self.reg_name()}")

            if name in used:
                raise DataformatError(f"Parameter {name} already used, endpoint: {self.reg_name()}")

            c_attr = all_attr_list[name]
            if c_attr.validate(value) == False:
                raise DataformatError(f"Illegal value of '{name}' parameter, endpoint: {self.reg_name()}")

            setattr(self, c_attr.getVarName(name), value)

            used[name] = 1

        # Set none for attributes that has been not mentioned in configuration
        for name, attr in all_attr_list.items():
            if name in used:
                continue

            def_value = attr.getDefaultValue()

            if attr.isObligatory() and def_value == None:
                raise CallError(f"'{name}' is obligatory but value is missing, endpoint: {self.reg_name()}")

            setattr(self, attr.getVarName(name), def_value)

        self._id = str(Endpoint._id) + "" + self.reg_name()
        Endpoint._id += 1
        self._srv = None
        self.__attr_list = all_attr_list

    def id( self ):
        return self._id

    @abstractmethod
    def identificator(self):
        pass

    def shortname(self):
        pass

    def match(self, pattern: str) -> bool:
        if len(pattern) < 3:
            raise CallError(f"Patter must be at leas 3 character long, but found: {pattern}")

        if pattern == self.reg_name():
            return True

        pattern = pattern.lower()

        if self.name().lower().find(pattern) != -1:
            return True

        for name, value in self.__attr_list.items():
            attr = getattr(self, value.name)
            if attr == None:
                continue

            if attr.lower().find(pattern) != -1:
                return True

        return False
    @abstractmethod
    def info(self):
        pass

    @abstractmethod
    def _getService(self, mode: Mode):
        pass

    def getService(self, mode: Mode):
        if self._srv == None:
            self._srv = self._getService(mode)

        return self._srv

    def add(self, ep):
        self.__ep.append(ep)

    def integrations(self):
        return self.__ep
