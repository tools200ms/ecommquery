
class SimpleDescription:
    class Generator:
        def __init__(self, langs = None):
            self.langs = langs

        def newDescription(self):
            return SimpleDescription(self.langs)

    def __init__(self, langs = None):
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

        # I'm setter:
        if self._def_lang == False:
            self._text = text
        else:
            self._text[lang] = text

    def getText(self):
        return self.text()

    def validate(self):
        pass
class HTMLDescription (SimpleDescription):
    class Generator(SimpleDescription.Generator):
        def __init__(self, sterilization = True, langs = None):
            super().__init__(langs)

        def newDescription(self):
            return HTMLDescription(self.langs)

    def __init__(self, langs = None):
        super().__init__( langs )

