from abc import abstractmethod


class ManagementService:

    @abstractmethod
    def getProductList(self, criteria = None):
        pass

    @abstractmethod
    def getProduct(self, item_no):
        pass

    def commitUpdates(self):
        pass
