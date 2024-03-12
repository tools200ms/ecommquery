from ecommquery.lib.atomic.description import SimpleDescription, HTMLDescription
from ecommquery.lib.product import Product


class WPSProduct(Product):

    def __init__(self, soup):
        self.__raw = soup

        self._name = SimpleDescription.Generator().newDescription()
        self._name.text(soup.select_one('h1 b').text.strip())

        self._description = HTMLDescription.Generator().newDescription()

        descr = soup.select_one('div.vc_column-inner div.wpb_wrapper div.wpb_text_column.wpb_content_element div.wpb_wrapper')

        self._description.text( descr.text )

        soup.select('div.woocommerce-product-gallery__image.flex-active-slide a')

    def getRaw(self):
        return self.__raw

    def getItemNo(self):
        return self._item_no

    def name( self, lang = None ):
        return self._name.text( None, lang )

    def description( self, value = None, lang = None ):
        return self._description.text( value, lang )

    def images(self):
        img_ids = []
        for img in self.__getImgIdArr():
            if 'id' not in img:
                continue
            img_ids.append(img['id'])

        return img_ids

    def defImage(self, img_id=None):
        pass
