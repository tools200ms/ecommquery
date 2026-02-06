from ecommquery.db.map.Checkout import ObjCheckout
from ecommquery.db.map.Object import Obj
from ecommquery.db.map.View import ObjCombLatestView, ObjTextLatestView, ObjIntLatestView
from ecommquery.db.map.definitions.Property import PropDef
from ecommquery.db.map.Property import ObjPropInt, ObjPropText


class MisoDataType:
    @staticmethod
    def determinateType(prop_d: PropDef):
        if str(prop_d.type).upper() == 'T':
            return MisoTextType
        elif str(prop_d.type).upper() == 'I':
            return MisoIntType

        raise Exception('Unknown type')

class MisoIntType(MisoDataType):
    OBJ_LATEST_VIEW_CLASS = ObjIntLatestView
    OBJ_PROP_CLASS = ObjPropInt

class MisoTextType(MisoDataType):
    OBJ_LATEST_VIEW_CLASS = ObjTextLatestView
    OBJ_PROP_CLASS = ObjPropText

class MisoObject:
    __cache_view_objs = {}

    def __init__(self, obj:Obj = None):
        if obj is None:
            obj = Obj.create()
            # invalidate casche
            self.__class__.__cache_view_objs = {}

        self._obj = obj
        self._checkout = None

        self.__cache_prop_list = None

    @property
    def id(self):
        return self._obj.id

    @classmethod
    def createNew(cls, key_prop, value, checkout):
        mobj = cls()
        mobj.setCheckout(checkout)
        mobj.update(key_prop, value)
        return mobj

    @classmethod
    def get(cls, propd:PropDef, key:int|str, unique = True):
        label = propd.label()
        if label not in cls.__cache_view_objs:
            cls.__cache_view_objs[label] = None

        # take value from memcache
        if cls.__cache_view_objs[label] is not None:
            cache = cls.__cache_view_objs[label]
        else:
            cache = {}
            cls.__cache_view_objs[label] = cache

            view_class = MisoTextType.determinateType(propd).OBJ_LATEST_VIEW_CLASS
            for obj_comb in (
                    view_class.select().where(view_class.prop == propd)):
                if unique:
                    cache[obj_comb.value] = obj_comb.obj_id
                else:
                    if obj_comb.value in cache:
                        cache[obj_comb.value].append(obj_comb.obj_id)
                    else:
                        cache[obj_comb.value] = [obj_comb.obj_id]

        if key in cache:
            obj_ids = cache[key]
        else:
            return None if unique else []

        if unique:
            obj = Obj.get(Obj.id == obj_ids)
            return MisoObject(obj)
        # else
        res = []
        for id in obj_ids:
            res.append(MisoObject(Obj.get(Obj.id == id)))

        return res

    # set a new checkout
    def setCheckout(self, checkout: ObjCheckout):
        self._checkout = checkout
        self.__cache_prop_list = None

    def _cache_properties(self):
        self.__cache_prop_list = {}
        for obj_l_view in (
                ObjIntLatestView.select().where(ObjIntLatestView.obj == self._obj)):
            self.__cache_prop_list[obj_l_view.prop.id] = obj_l_view.value
        for obj_l_view in (
                ObjTextLatestView.select().where(ObjTextLatestView.obj == self._obj)):
            self.__cache_prop_list[obj_l_view.prop.id] = obj_l_view.value

    def getValue(self, prop_d:PropDef) -> str|int:
        if self.__cache_prop_list is None:
            self._cache_properties()

        if prop_d.id in self.__cache_prop_list:
            return self.__cache_prop_list[prop_d.id]

        return None

    def update(self, prop_d:PropDef, value:str|int):
        data_type = MisoTextType.determinateType(prop_d)
        #obj_view_latest = data_type.OBJ_LATEST_VIEW_CLASS
        obj_prop_class = data_type.OBJ_PROP_CLASS

        if self.__cache_prop_list is None:
            self._cache_properties()

        if prop_d.id in self.__cache_prop_list:
            if self.__cache_prop_list[prop_d.id] == value:
                print("# no update needed")
                return

        # Update
        obj_prop_class.create(
            checkout=self._checkout,
            obj=self._obj, prop=prop_d, value=value)

        # update cache
        self.__cache_prop_list[prop_d.id] = value
