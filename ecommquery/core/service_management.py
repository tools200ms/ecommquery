from abc import abstractmethod


class ManagementService:

    def establish(self):
        pass

    def test(self):
        pass

    def id(self)-> str:
        pass

    @abstractmethod
    def getProductList(self, criteria = None):
        pass

    @abstractmethod
    def getProduct(self, item_no):
        pass

    def commitUpdates(self):
        pass
