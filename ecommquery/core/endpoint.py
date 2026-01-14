from typing import Callable

from abc import abstractmethod

from ecommquery.core.validators import Validator, ParamValidator
from ecommquery.ecommquery import Mode
from ecommquery.exceptions import DataformatError, CallError


class Endpoint:
    class Constr:

        def __init__( self,
                      validator: ParamValidator | Callable[[str], bool],
                      obligatory: bool = True,
                      # Alternative name for the attribute in case of name conflicts
                      alt_name: str = None, is_secret = False ):

            
            if isinstance(validator, type):
                validator = validator()

            if isinstance(validator, ParamValidator):
                self.validate = validator.validate
                self.getDefaultValue = validator.getDefaultValue
            else:
                self.validate = lambda value: (validator(value), value)
                self.getDefaultValue = lambda: None

            self.__obligatory = obligatory
            self._alt_name = alt_name
            self._is_secret = is_secret

        def getVarName(self, name: str):
            pref = '__' if self._is_secret else '_'

            if self._alt_name is None:
                return pref + name

            return pref + self._alt_name

        def isObligatory(self):
            return self.__obligatory
        
        def isSecret(self):
            return self._is_secret

    __loaded = {}
    _id = 0

    @staticmethod
    def register(ep_class, srv_class = None):
        Endpoint.__loaded[ep_class.reg_name()] = (ep_class, srv_class);

    @staticmethod
    def getClass(ep_name):
        #global endpointtypes
        if not ep_name in Endpoint.__loaded:

            raise Exception(f"""Endpoint of '{ep_name}' has not been defined.
    Avialable modules: 
      - {"\n      - ".join(Endpoint.__loaded.keys())}
""")

        return Endpoint.__loaded[ep_name][0]

    @staticmethod
    def getEpName(srv_class):
        for ep_name, ep_info in Endpoint.__loaded.items():
            if ep_info[1] == srv_class:
                return ep_name

        raise Exception('Endpoint of \'' + srv_class + '\' has not been defined')

    @staticmethod
    @abstractmethod
    def reg_name() -> str:
        pass

    @staticmethod
    @abstractmethod
    def name() -> str:
        pass

    def __init__( self, attr_list : {}, params : {}, id:str ):
        comm_attr_list = {'memo': Endpoint.Constr(Validator.text, False)}

        all_attr_list = comm_attr_list | attr_list

        used = {}

        for name, value in params.items():
            if name not in all_attr_list:
                raise DataformatError(f"Parameter {name} not supported, endpoint: {self.reg_name()}")

            if name in used:
                raise DataformatError(f"Parameter {name} already used, endpoint: {self.reg_name()}")

            c_attr = all_attr_list[name]
            res, norm_value = c_attr.validate(value)
            if res == False:
                raise DataformatError(f"Illegal value of '{name}' parameter, endpoint: {self.reg_name()}")

            # if hasattr(c_attr, 'normValue'):
            #     # normalize value:
            #     value = c_attr.normValue()

            if not c_attr.isSecret():
                setattr(self, c_attr.getVarName(name), norm_value)
            else:
                setattr(self,
                        f"_{self.__class__.__name__}{c_attr.getVarName(name)}",
                        norm_value)

            used[name] = 1

        self.__attr_list = {}
        # Set none for attributes that has been not mentioned in configuration
        for name, attr in all_attr_list.items():
            if name in used:
                continue

            def_value = attr.getDefaultValue()

            if attr.isObligatory() and def_value == None:
                raise CallError(f"'{name}' is obligatory but value is missing, endpoint: {self.reg_name()}")

            setattr(self, attr.getVarName(name), def_value)

            if not attr.isSecret():
                self.__attr_list[name] = attr

        if id is not None:
            self._local_id = id
        else:
            self._local_id = str(self.__class__._id)
            self.__class__._id += 1

        self._id = f"{self.reg_name()}.{self._local_id}"

        self._srv = None

    @property
    def local_id(self)->str:
        return self._local_id

    @property
    def id(self)->str:
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
            attr = getattr(self, value.getVarName(name))
            if attr == None:
                continue

            if isinstance(attr, str) and attr.lower().find(pattern) != -1:
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
