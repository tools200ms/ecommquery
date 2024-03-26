from abc import abstractmethod


class Endpoint:
    __endpointtypes = {}
    _id = 0

    @staticmethod
    def register(ep_class):
        Endpoint.__endpointtypes[ep_class.reg_name()] = ep_class;

    @staticmethod
    def getClass(type):
        #global endpointtypes
        if not type in Endpoint.__endpointtypes:
            raise Exception('Endpoint of \'' + type + '\' has not been defined')

        return Endpoint.__endpointtypes[type]

    @staticmethod
    @abstractmethod
    def factory( params ):
        pass

    @staticmethod
    @abstractmethod
    def reg_name():
        pass

    def __init__(self, ep_set, memo = None):
        self._memo = memo

        self._id = Endpoint._id
        Endpoint._id += 1

    def id(self):
        return self._id

    @abstractmethod
    def identificator(self):
        pass

    @abstractmethod
    def name(self):
        pass

    def shortname(self):
        pass

    @abstractmethod
    def match(self, pattern: str) -> bool:
        pass

    @abstractmethod
    def info(self):
        pass

    @abstractmethod
    def getService(self):
        pass

    def add(self, ep):
        self.__ep.append(ep)

    def integrations(self):
        return self.__ep
