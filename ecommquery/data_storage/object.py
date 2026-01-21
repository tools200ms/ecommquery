from ecommquery.db.map.Checkout import ObjCheckout
from ecommquery.db.map.Object import Obj
from ecommquery.db.map.View import ObjCombLatestView, ObjTextLatestView, ObjIntLatestView
from ecommquery.db.map.definitions.Property import PropDef


class MisoObject:

    def __init__(self, obj:Obj):
        self._obj = obj
        self._checkout = None

    __cache_view_objs = {}

    @classmethod
    def get(cls, propd:PropDef, key:int|str):
        label = propd.label()
        if label not in cls.__cache_view_objs:
            cls.__cache_view_objs[label] = None

        # take value from memcache
        if cls.__cache_view_objs[label] is not None:
            cache = cls.__cache_view_objs[label]
        else:
            cache = {}
            cls.__cache_view_objs[label] = cache

            if str(propd.type).upper() == 'T':
                view_class = ObjTextLatestView
            else:
                view_class = ObjIntLatestView

            for obj_comb in (
                    view_class.select().where(view_class.prop == propd)):
                cache[obj_comb.valuei] = obj_comb.obj_id

        if key in cache:
            obj_id = cache[key]
        else:
            return None

        obj = Obj.get(Obj.id == obj_id)

        return MisoObject(obj)

    def setCheckoutPoll(self, checkout: ObjCheckout):
        self._checkout = checkout

    def update(self, prop:PropDef, value:str|int):
        pass

