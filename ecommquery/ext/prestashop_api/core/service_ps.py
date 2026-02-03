from pprint import pprint

from ecommquery.core.service_management import ManagementService
from ecommquery.ext.prestashop_api.lib.ps_feature import PSFeature, PSFeatureValue
from ecommquery.ext.prestashop_api.lib.ps_options import PSOption, PSOptionValue
from ecommquery.ext.prestashop_api.lib.ps_product import PSProduct
from ecommquery.ext.prestashop_api.lib.ps_stock import PSStock
from ecommquery.lib.functions.url import URLFun
from prestapyt import PrestaShopWebServiceDict


class DummySession:
    def request(self, *args, **kwargs):
        raise RuntimeError("Session not initialized")

    def close(self):
        pass

class ServicePS(ManagementService, PrestaShopWebServiceDict):

    def __init__(self, api_url, api_key, verbose: bool, debug: bool, pretend: bool):
        session = None
        if pretend:
            session = DummySession
        super().__init__(api_url, api_key, debug = debug, session = session, verbose = verbose)
        self._pretend = pretend

    def test(self):
        res = self.get('shops')

        if 'shops' in res:
            res = res['shops']
            print(f"Fount {len(res)} shop(s): ")
            for shop in res:
                shop_id = res[shop]['attrs']['id']
                shop_res = self.get('shops', shop_id)
                if not 'shop' in shop_res:
                    raise Exception("Data integrity error")

                shop_res = shop_res['shop']
                print(f"    #{shop_id}: '{shop_res['name']}', shop is {'active' if shop_res['active'] == '1' else 'NOT active'}")
        else:
            raise Exception("No 'shops' key found in response")

    def reestablish(self):
        return self.__class__(self._api_url, self._api_key, debug = self.debug, verbose = self.verbose, pretend = self._pretend)

    def close(self):
        self.client.close()
        self.client = None

    # example criteria filtering:
    # criteria = {'filter[id_category_default]': '269'}
    def getProductList(self, criteria = None):
        if criteria != None:
            res = self.search('products', options = criteria)
        else:
            res = self.search('products')

        return res

    def getProductListByCategories(self, cat_id:int|list|tuple):

        prod_ids = []

        if isinstance(cat_id, list|tuple):
            for cid in cat_id:
                prod_ids += self.getProductListByCategories( cid )

            return prod_ids

        res = self.get('categories', cat_id )


        if 'category' not in res:
            raise Exception( 'Missing data (category)' )

        for prod_id in res['category']['associations']['products']['product']:
            prod_ids.append(prod_id['id'])

        return prod_ids

    def getProduct( self, item_no ):
        return PSProduct( self.get( 'products', item_no ) )

    def getStock(self, item_no):
        return PSStock(self.get( 'stock_availables', item_no))

    def getFeatures(self):
        feat_raw_list = PSFeature.getProductFeaturesList(self.get('product_features'))
        feat_list = {}
        feat_list_by_key = {}

        from pprint import pprint
        for feat_raw in feat_raw_list:
            feat = PSFeature(self.get('product_features', feat_raw['attrs']['id']))
            feat_list[feat.id] = feat
            feat_list_by_key[URLFun.key_friendly_str(feat.text())] = feat

        for featval_raw in PSFeature.getProductFeatureValuesList(self.get('product_feature_values')):

            feat_val = PSFeatureValue(self.get('product_feature_values', featval_raw['attrs']['id']))
            feat_list[feat_val.id_feature].addValue(feat_val)

        return feat_list_by_key

    def getOptions(self):
        opt_raw_list = self.get('product_options')
        opt_list = {}
        opt_list_by_key = {}

        for opt_raw in opt_raw_list:
            opt = PSOption(opt_raw)

        for optval_raw in PSOption.getProductOptionValuesList(self.get('product_option_values')):

            opt_val = PSOptionValue(None)

        return opt_list_by_key

    def commitStock(self, stock):
        changes = stock.prepareToCommit()
        if changes != False:
            self.edit('stock_availables', stock.getRaw())

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
