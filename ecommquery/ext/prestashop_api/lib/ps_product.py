from ecommquery.ecommquery import ECommDef
from ecommquery.lib.atomic.description import SimpleDescription, HTMLDescription
from ecommquery.lib.product import Product

class PSProduct(Product):
    def __init__(self, raw):
        self.__raw = raw

        if 'product' not in raw:
            raise Exception('Missing data (product)')

        self.__raw_prod_buf = raw['product']

        self._item_no = raw['product']['id']
        self._name = SimpleDescription.Generator().newDescription()
        self._name.text( raw['product']['name']['language']['value'] )

        self._description = HTMLDescription.Generator().newDescription()
        self._description.text( raw['product']['description']['language']['value'] )

        # self._short_description = HTMLDescription.Generator().newDescription()
        # self._short_description = ...

    def getRaw(self):
        return self.__raw

    def getItemNo(self):
        return self._item_no

    def name( self, value = None, lang = None ):
        return self._name.text( value, lang )

    def description( self, value = None, lang = None ):
        return self._description.text( value, lang )


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

        self.__raw_prod_buf['name']['language']['value'] = self.name()
        self.__raw_prod_buf['description']['language']['value'] = self.description()

