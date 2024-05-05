from ecommquery.lib.atomic.description import SimpleDescription, HTMLDescription
from ecommquery.lib.product import Product


class WEBProduct(Product):

    def __init__(self, soup):
        super().__init__()

        self.__raw = soup

        self._name.text(soup.select_one('h1 b').text.strip())

        descr = soup.select_one('div.vc_column-inner div.wpb_wrapper div.wpb_text_column.wpb_content_element div.wpb_wrapper')
        self._descr.text( descr.text )

        soup.select('div.woocommerce-product-gallery__image.flex-active-slide a')

    def getRaw(self):
        return self.__raw

    def getItemNo(self):
        return self._item_no

    def name( self, lang = None ):
        return self._name.text( None, lang )

    def images(self):
        img_ids = []
        for img in self.__getImgIdArr():
            if 'id' not in img:
                continue
            img_ids.append(img['id'])

        return img_ids

    def defImage(self, img_id=None):
        pass
