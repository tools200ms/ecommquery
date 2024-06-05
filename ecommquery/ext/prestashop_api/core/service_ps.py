from ecommquery.core.service_management import ManagementService
from ecommquery.ext.prestashop_api.lib.ps_feature import PSFeature, PSFeatureValue
from ecommquery.ext.prestashop_api.lib.ps_options import PSOption, PSOptionValue
from ecommquery.ext.prestashop_api.lib.ps_product import PSProduct
from ecommquery.lib.functions.url import URLFun
from prestapyt import PrestaShopWebServiceDict


class ServicePS(ManagementService, PrestaShopWebServiceDict):

    def __init__(self, api_url, api_key, verbose: bool, debug: bool, pretend: bool):
        super().__init__(api_url, api_key, debug = debug, session = None, verbose = verbose)

    # example criteria filtering:
    # criteria = {'filter[id_category_default]': '269'}
    def getProductList(self, criteria = None):
        if criteria != None:
            res = self.search('products', options = criteria)
        else:
            res = self.search('products')

        return res

    def getProduct(self, item_no):
        return PSProduct(self.get('products', item_no))

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
