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
                raise CallError('Empty Endpoint set')

            ep_dict_search = None
            ep = None

            if id == None:
                ep_dict_search = self.__ep_dict
            else:
                if id in self.__ep_dict:
                    ep_dict_search[id] = self.__ep_dict[id]
                else:
                    raise CallError(f"No endpoint with given Id has been found: {id}")

            if pattern != None:
                for ep_i in ep_dict_search.values():
                    if ep_i.match(pattern):
                        if ep == None:
                            ep = ep_i
                        else:
                            raise CallError('Multiple matches for Endpoint')
            elif len(ep_dict_search) == 1:
                ep = list(ep_dict_search.values())[0]
            else:
                raise CallError('Multiple endpoint elements but no Id nor unque pattern has been provided')

            # ep is of a None type if no endpoint has been found/mached
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
