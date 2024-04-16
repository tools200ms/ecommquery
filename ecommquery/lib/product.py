from abc import abstractmethod

class Product:

    def getItemNo(self):
        return self._item_no

    # Return product's name, if name is empty, empty string is '
    # returned
    def name(self, value = None, lang = None):
        return self._name.text(value, lang)

    # Return String with short description, string might be an HTML code
    # if short desription is empty, an empty string is returned
    def sdescr(self, value=None, lang=None):
        return self._sdescr.text(value, lang)

    def getSDescr(self):
        return self._sdescr

    def getDescr(self):
        return self._descr

    # Return String with description, string might be an HTML code
    # if desription is empty, an rmpty string is returned
    def descr(self, value=None, lang=None):
        return self._descr.text(value, lang)

    def fdescr(self, lang=None):
        # HTMLDescription
        sdesc = self._sdescr.text(None, lang)
        desc = self._descr.text(None, lang)

        if len(sdesc) != 0 and len(desc) != 0:
            sep = '\n<hr>\n'
        else:
            sep = ''

        return sdesc + sep + desc
