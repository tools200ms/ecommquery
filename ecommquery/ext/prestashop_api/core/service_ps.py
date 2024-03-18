from ecommquery.core.service import Service
from ecommquery.ext.prestashop_api.lib.ps_product import PSProduct
from prestapyt import PrestaShopWebServiceDict


class ServicePS(Service, PrestaShopWebServiceDict):
    def getProductList(self, criteria = None):
        if criteria != None:
            res = self.search('products', options = criteria)
        else:
            res = self.search('products')

        return res

    def getProduct(self, item_no):
        return PSProduct(self.get('products', item_no))

    def commitProduct(self, prod):
        changes = prod.prepareToCommit()
        if changes != False:
            self.edit('products', prod.getRaw())
        # if there has been no changes don't attempt to call API

    def uploadImage(self, file_name, prod):
        fd = open('data/' + file_name, "rb")
        content = fd.read()
        fd.close()

        self.add('/images/products/' + prod.getItemNo(),
                 files=[('image', file_name, content)])
