from abc import abstractmethod

from ecommquery.lib.functions.html import HTMLfun


class Product:
    def __init__(self):
        self._item_no = None
        self._name = None
        self._sdescr = None
        self._descr = None
        self.variant = None

    def do_descr_norm(self, lang = None):
        html_text = self._descr.text(lang=lang)

        html_text_out, stat = HTMLfun.sanitize(html_text)

        self._descr.text(text = html_text_out, lang = lang)

        return stat

