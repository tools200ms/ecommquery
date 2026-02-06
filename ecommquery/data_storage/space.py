from ecommquery.db.map.definitions.Property import PropDef
from ecommquery.db.map.definitions.Space import SpcDef

class PropertyMap:
    def __init__(self, spc):
        for propdef in PropDef.select().where(PropDef.spc == spc):
            self.__dict__[propdef.ref_name] = propdef

class Space:
    class Partition:
        def __init__(self, part, space):
            self._part = part
            self.name = part.name
            self.space = space

        @property
        def part(self):
            return self._part

    global_properties = None

    def __init__(self, spc):
        self._spc = spc
        self.properties = PropertyMap(spc)
        if self.__class__.global_properties is None:
            self.__class__.global_properties = PropertyMap(None)
    
    def partitions(self, filter:str):
        f_part = {}
        for p in self._spc.parts:
            if filter is None or filter in p.name:
                f_part[p.name] = Space.Partition(p, self)

        return f_part

    @classmethod
    def getSpaces(cls, filter: str = None):
        f_space = {}

        if filter is None:
            it = SpcDef.select()
        else:
            it = SpcDef.select().where(SpcDef.name.contains(filter))

        for s in it:
            f_space[s.name] = Space(s)

        return f_space

