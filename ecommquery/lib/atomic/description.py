from ecommquery.lib.atomic.atomic import Atomic

class SimpleDescription (Atomic):
    class Translations:
        def __init__(self, langs = None):
            self.langs = langs

        def newDescription(self):
            return SimpleDescription(self.langs)

    def __init__(self, langs = None):
        super().__init__()

        if langs == None or len(langs) == 0:
            self._text = None
            self._def_lang = False
        else:
            self._text = []

            for l in langs:
                self._text[l] = None

            self._def_lang = None

    def setDefLang(self, lang):
        self._def_lang = lang

    def text(self, text = None, lang = None):
        if lang == None:
            lang = self._def_lang

        # I'm getter:
        if text == None:
            if lang == False:
                return self._text
            else:
                return self._text[self._def_lang]

        # I'm a setter:
        if self._def_lang == False:
            if self._text != None:
                self.markChange()

            self._text = text
        else:
            if self._text[lang] != None:
                self.markChange()

            self._text[lang] = text

    def getText(self):
        return self.text()

    def validate(self):
        pass
class HTMLDescription (SimpleDescription):
    class Translations( SimpleDescription.Translations ):
        def __init__(self, sterilization = True, langs = None):
            super().__init__(langs)

        def newDescription(self):
            return HTMLDescription(self.langs)

    def __init__(self, langs = None):
        super().__init__( langs )

