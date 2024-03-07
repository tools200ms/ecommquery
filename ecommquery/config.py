from abc import abstractmethod
from prestapyt import PrestaShopWebServiceDict

class GlobalConfig:
    _id = 0
    def __init__(self, memo):
        self.memo = memo
        self.configs = []
        self._id = GlobalConfig._id
        GlobalConfig._id += 1

    def id(self):
        return self._id

    @abstractmethod
    def endPoint(self):
        pass

    @abstractmethod
    def info(self):
        pass

    @abstractmethod
    def getService(self):
        pass

    def add(self, conf):
        self.configs.append(conf)

    def integrations(self):
        return self.configs

class ConfigPS(GlobalConfig):
    def __init__(self, url, key, memo):
        super().__init__(memo)
        self.url = url
        self.key = key

    def endPoint(self):
        return "PrestaShop"

    def info(self):
        info = self.url
        if self.memo != None: info += "\n" + self.memo

        return info

    def getService(self):
        return PrestaShopWebServiceDict( self.url, self.key, verbose=False )
