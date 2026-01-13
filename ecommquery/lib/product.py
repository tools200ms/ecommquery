from ecommquery.lib.atomic.description import HTMLDescription, SimpleDescription
from ecommquery.lib.functions.html import HTMLfun


class Product:

    def __init__(self, name: str = None, sdescr: str = None, descr: str = None):
        self._def_lang_code = None

        self._name = SimpleDescription.Translations().newDescription()
        self._sdescr = HTMLDescription.Translations().newDescription()
        self._descr = HTMLDescription.Translations().newDescription()

        if name != None: self._name.text(name)
        if sdescr != None: self._sdesrc.text(sdescr)
        if descr != None: self._descr.text(descr)

    @property
    def getItemNo(self):
        return self._item_no

    def get_lang(self):
        return self._def_lang_code

    def set_lang(self, code):
        self._def_lang_code = code

    lang = property(get_lang, set_lang)

    def getName(self) -> SimpleDescription:
        return self._name

    def get_name(self) -> str:
        return self._name.text(None, self._def_lang_code)

    def set_name(self, value):
        self._name.text(value, self._def_lang_code)

    name = property(get_name, set_name)

    def getSDescr(self) -> HTMLDescription:
        return self._sdescr

    def get_sdescr(self):
        return self._sdescr.text(None, self._def_lang_code)

    def set_sdescr(self, value):
        self._sdescr.text(value, self._def_lang_code)

    sdescr = property(get_sdescr, set_sdescr)

    def getDescr(self) -> HTMLDescription:
        return self._descr

    def get_descr(self):
        return self._descr.text(None, self._def_lang_code)

    def set_descr(self, value):
        self._descr.text(value, self._def_lang_code)

    descr = property(get_descr, set_descr)

    def cdescr_variant(self, lang) -> str:
        # HTMLDescription
        sdesc = self._sdescr.text(None, lang)
        desc = self._descr.text(None, lang)

        if len(sdesc) != 0 and len(desc) != 0:
            sep = '\n<hr>\n'
        else:
            sep = ''

        return sdesc + sep + desc

    @property
    def cdescr(self):
        return self.cdescr_variant(self._def_lang_code)

class PlainTextProduct(Product):
    def __init__(self, prod):
        self.prod = prod

        # Make sure it's senitized:
        HTMLfun.sanitize_html(prod.getDescr())
        HTMLfun.sanitize_html(prod.getSDescr())

    def get_name(self) -> str:
        return self.prod.get_name()

    name = property(get_name)

    def get_sdescr(self):
        return HTMLfun.getPlainTextSuper(self.prod.get_sdescr())
        # return HTMLfun.getStripedText()

    sdescr = property(get_sdescr)

    def get_descr(self):
        return HTMLfun.getPlainTextSuper(self.prod.get_descr())
        #return HTMLfun.getStripedText(self.prod.get_descr())

    descr = property(get_descr)

    def cdescr_variant(self) -> str:
        # HTMLDescription
        sdesc = self.sdescr
        desc = self.descr

        if len(sdesc) != 0 and len(desc) != 0:
            sep = '\n\n'
        else:
            sep = ''

        return sdesc + sep + desc

    @property
    def cdescr(self):
        return self.cdescr_variant()
