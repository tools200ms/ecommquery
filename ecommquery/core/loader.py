from abc import abstractmethod

from ecommquery.exceptions import CallError


class Loader:
    class Config:
        def __init__(self, memo, name):
            self._memo = memo
            self._name = name
            self.__ep_dict = {}

        def getName(self):
            return self._name

        def endpointNo(self):
            return len( self.__ep_dict )
        def addEndpoint(self, ep):
            self.__ep_dict[ep.id()] = ep

        def endpoint(self, id = None, pattern : str = None):
            if len(self.__ep_dict) == 0:
                raise Loader.CallError('Empty Endpoint set')

            ep = None

            if id == None and len(self.__ep_dict) == 1:
                ep = list(self.__ep_dict.values())[0]
            elif id == None and pattern == None:
                raise CallError('Multiple endpoint elements but no Id has been provided')
            elif id != None:
                if id in self.__ep_dict:
                    ep = self.__ep_dict[id]
                else:
                    raise Loader.CallError('No endpoint with given Id has been found')
            elif pattern != None:
                for ep_i in self.__ep_dict.values():
                    if ep_i.match(pattern):
                        if ep == None:
                            ep = ep_i
                        else:
                            raise CallError('Multiple matches for Endpoint')
                # ep can be None if no patter mach has been found
            else:
                raise CallError('Wrong data type, endpoint can be indicated by name, partial name or Id')

            return ep

        def endpoints(self):
            return self.__ep_dict.values()

    def __init__(self):
        pass

    @abstractmethod
    def getInfo(self):
        pass

    @abstractmethod
    def readConfig(self):
        pass

    @abstractmethod
    def saveConfig(self):
        pass
