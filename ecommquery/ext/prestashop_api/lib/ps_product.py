from ecommquery.ecommquery import ECommDef
from ecommquery.exceptions import ExternalResourceAccessError
from ecommquery.ext.prestashop_api.lib.atomic.ps_number import PSNumber
from ecommquery.lib.atomic.description import SimpleDescription, HTMLDescription
from ecommquery.lib.product import Product

class PSProduct(Product):
    def __init__( self, raw ):
        super().__init__()

        self.__raw = raw

        if 'product' not in raw:
            raise Exception( 'Missing data (product)' )

        self.__raw_prod_buf = raw['product']
        self.__raw_assoc_buf = self.__raw_prod_buf['associations']

        if 'product_features' in self.__raw_assoc_buf:
            self._features = self.__raw_assoc_buf['product_features']
            self._feature_changed = False

        self._item_no = self.__raw_prod_buf['id']

        self._name.text( self.__raw_prod_buf['name']['language']['value'] )
        self._sdescr.text( self.__raw_prod_buf['description_short']['language']['value'] )
        self._descr.text( self.__raw_prod_buf['description']['language']['value'] )

        self._price = PSNumber()
        self._price.rawValue( self.__raw_prod_buf['price'] )

        self._weight = PSNumber()
        self._weight.rawValue( self.__raw_prod_buf['weight'] );

        # self._short_description = HTMLDescription.Generator().newDescription()
        # self._short_description = ...


    # append
    def set_features(self, list: []):

        if 'product_feature' in self._features:
            clist = self._features['product_feature']
        else:
            clist = []

        if len(list) != 0:
            self._features['product_feature'] = clist + list
            self._feature_changed = True

    def getRaw(self):
        return self.__raw


    def price(self, price = None):
        return self._price.value(price)

    def weight(self, weight = None):
        return self._weight.value(weight)

    def get_def_cat(self):
        return self.__raw_prod_buf['id_category_default']

    def set_def_cat(self, value):
        raise Exception("Not implemented!")
        raw_cat_list = self.__raw_prod_buf['associations']['categories']['category']
        cat_list = {}

        # validate cat. list
        for cat in raw_cat_list:
            c_id = cat['id']
            if c_id in cat_list:
                raise ExternalResourceAccessError(f"Duplicated category id ({c_id}) for item: {self._item_no}")
            cat_list[c_id] = {}

        if value not in cat_list:
            raise ExternalResourceAccessError(
                f"Data inconsistency, default category has not been found, item id: {self._item_no}, failed cat_id: {search_cat}")

        # setter
        self.__raw_prod_buf['id_category_default'] = value

    def_cat = property(get_def_cat, set_def_cat)

    def __getImgIdArr(self):
        if 'associations' not in self.__raw_prod_buf or 'images' not in self.__raw_prod_buf['associations']:
            return

        raw_imgs_buf = self.__raw_prod_buf['associations']['images']

        if 'attrs' not in raw_imgs_buf:
            if 'image' not in raw_imgs_buf:
                return
            else:
                raise Exception('Incorrect dataset (product images - missing \'attrs\')')
        elif 'image' not in raw_imgs_buf:
                raise Exception('Incorrect dataset (product images - missing \'image\')')

        if type(raw_imgs_buf['image']) == list:
            return raw_imgs_buf['image']
        else:
            return [raw_imgs_buf['image']]
    def images(self):
        img_ids = []
        for img in self.__getImgIdArr():
            if 'id' not in img:
                continue
            img_ids.append(img['id'])

        return img_ids

    def rmImage(self, id):
        new_img_arr = []
        rm_img_found = False
        set_next_def_img = False

        for img in self.__getImgIdArr():
            if img['id'] == id:
                rm_img_found = True
                if id == self.defImage():
                    set_next_def_img = True
                continue

            if set_next_def_img == True:
                set_next_def_img = img['id']

            new_img_arr.append(img)

        if rm_img_found == False:
            return

        new_img_arr_len = len(new_img_arr)

        if type(set_next_def_img) == str:
            self.defImage(set_next_def_img)
        elif set_next_def_img == True:
            if new_img_arr_len > 0:
                self.defImage(new_img_arr[0]['id'])
            else:
                self.defImage(ECommDef.Unset)

        if new_img_arr_len > 1:
            self.__raw_prod_buf['associations']['images']['image'] = new_img_arr
        elif new_img_arr_len == 1:
            self.__raw_prod_buf['associations']['images']['image'] = new_img_arr[0]
        else:
            self.__raw_prod_buf['associations']['images']['image'] = {}

    def getDefImage(self):
        if 'id_default_image' not in self.__raw_prod_buf:
            return

        def_img = self.__raw_prod_buf['id_default_image']

        if 'attrs' not in def_img:
            if 'value' not in def_img:
                return
            else:
                raise Exception('Incorrect dataset (product id_default_image - missing \'attrs\')')
        elif 'value' not in def_img:
            raise Exception('Incorrect dataset (product id_default_image - missing \'value\')')

        return def_img['value']

    def setDefImage(self, img_id):
        if 'id_default_image' not in self.__raw_prod_buf:
            self.__raw_prod_buf['id_default_image'] = {}

        if 'value' not in self.__raw_prod_buf['id_default_image']:
            self.__raw_prod_buf['id_default_image']['value'] = None

        if img_id not in self.images():
            return False

        self.__raw_prod_buf['id_default_image']['value'] = img_id
        return True

    def unSetDefImage(self):
        if 'id_default_image' in self.__raw_prod_buf and \
           'value' in self.__raw_prod_buf['id_default_image']:
            del self.__raw_prod_buf['id_default_image']['value']
            self.__raw_prod_buf['id_default_image']['value'] = {}

    def defImage(self, img_id = None):
        if img_id == None:
            return self.getDefImage()

        if type(img_id) == str:
            return self.setDefImage(img_id)

        if img_id == ECommDef.Unset:
            return self.unSetDefImage()

    def prepareToCommit(self):
        if 'position_in_category' in self.__raw_prod_buf:
            del self.__raw_prod_buf['position_in_category']

        if 'manufacturer_name' in self.__raw_prod_buf:
            del self.__raw_prod_buf['manufacturer_name']

        if 'quantity' in self.__raw_prod_buf:
            del self.__raw_prod_buf['quantity']


        changes = []
        if self._name.hasChanged():
            changes.append(self._name.text)
            self.__raw_prod_buf['name']['language']['value'] = self._name.text()

        if self._sdescr.hasChanged():
            changes.append(self._sdescr.text)
            self.__raw_prod_buf['description_short']['language']['value'] = self._sdescr.text()

        if self._descr.hasChanged():
            changes.append(self._descr.text)
            self.__raw_prod_buf['description']['language']['value'] = self._descr.text()

        if self._price.hasChanged():
            changes.append(self._price.rawValue)
            self.__raw_prod_buf['price'] = self._price.rawValue()

        if self._weight.hasChanged():
            changes.append(self._weight.rawValue)
            self.__raw_prod_buf['weight'] = self._weight.rawValue()

        if self._feature_changed:
            pass


        return len(changes) != 0

