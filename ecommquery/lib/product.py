from abc import abstractmethod

class Product:

    def __init__(self):
        self._def_lang_code = None

    @property
    def getItemNo(self):
        return self._item_no

    def get_lang(self):
        return self._def_lang_code

    def set_lang(self, code):
        self._def_lang_code = code

    lang = property(get_lang, set_lang)

    # Return product's name, if name is empty, empty string is '
    # returned
    def name_variant(self, lang, value = None) -> str:
        return self._name.text(value, lang)

    def get_name(self) -> str:
        return self._name.text(None, self._def_lang_code)

    def set_name(self, value):
        self._name.text(value, self._def_lang_code)

    name = property(get_name, set_name)

    # Return String with short description, string might be an HTML code
    # if short desription is empty, an empty string is returned
    def sdescr_variant(self, lang, value=None) -> str:
        return self._sdescr.text(value, lang)

    def get_sdescr(self):
        return self._sdescr.text(None, self._def_lang_code)

    def set_sdescr(self, value):
        self._sdescr.text(value, self._def_lang_code)

    sdescr = property(get_sdescr, set_sdescr)

    # Return String with description, string might be an HTML code
    # if desription is empty, an rmpty string is returned
    def descr_variant(self, lang, value=None) -> str:
        return self._descr.text(value, lang)

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
