from ecommquery.lib.atomic.description import SimpleDescription, HTMLDescription
from ecommquery.lib.product import Product

class PSProduct(Product):
    def __init__(self, raw):
        self.raw = raw

        self._item_no = raw['product']['id']
        self._name = SimpleDescription.Generator().newDescription()
        self._name.text( raw['product']['name']['language']['value'] )

        self._description = HTMLDescription.Generator().newDescription()
        self._description.text( raw['product']['description']['language']['value'] )

        # self._short_description = HTMLDescription.Generator().newDescription()
        # self._short_description = ...

    def getItemNo(self):
        return self._item_no

    def name( self, value = None, lang = None ):
        return self._name.text( value, lang )

    def description( self, value = None, lang = None ):
        return self._description.text( value, lang )

    def getRaw(self):
        return self.raw

    def prepareToCommit(self):
        del self.raw['product']['position_in_category']
        del self.raw['product']['manufacturer_name']
        del self.raw['product']['quantity']

        self.raw['product']['name']['language']['value'] = self.name()
        self.raw['product']['description']['language']['value'] = self.description()

