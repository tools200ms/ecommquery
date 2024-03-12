from abc import abstractmethod

class LoaderParserError(Exception):
    pass

class Loader:
    class Config:
        def __init__(self, memo):
            self.memo = memo
            self.__ep_dict = {}

        def endpointNo(self):
            return len( self.__ep_dict )
        def addEndpoint(self, ep):
            self.__ep_dict[ep.id()] = ep

        def endpoint(self, id = None):
            if len(self.__ep_dict) == 0:
                raise Exception('Empty Endpoint set')
            ep = None

            if id == None and len(self.__ep_dict) == 1:
                ep = self.__ep_dict[0]
            elif id == None:
                raise Exception('Multiple endpoint elements but no Id has been provided')
            elif type(id) == int:
                if id in self.__ep_dict:
                    ep = self.__ep_dict[id]
                else:
                    raise Exception('No endpoint with given Id has been found')
            elif type(id) == str:
                for ep_i in self.__ep_dict.values():
                    if ep_i.reg_name() == id:
                        if ep == None:
                            ep = ep_i
                        else:
                            raise Exception('Multiple matches for Endpoint')
                if ep == None:
                    raise Exception('No endpoint matched')
            else:
                raise Exception('Wrong data type, endpoint can be indicated by name, partial name or Id')

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
