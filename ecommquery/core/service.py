from abc import abstractmethod


class Service:

    @abstractmethod
    def getProductList(self, criteria = None):
        pass

    @abstractmethod
    def getProduct(self, item_no):
        pass
