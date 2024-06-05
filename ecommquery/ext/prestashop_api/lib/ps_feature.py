from pprint import pprint

from ecommquery.exceptions import CallError
from ecommquery.lib.atomic.description import SimpleDescription
from ecommquery.lib.functions.url import URLFun


class PSFeatureValue:
    def __init__(self, raw):
        self._value = SimpleDescription.Translations().newDescription()

        p_feat_val = raw['product_feature_value']

        self._id = int(p_feat_val['id'])
        self._id_feature = int(p_feat_val['id_feature'])

        self._value.text(p_feat_val['value']['language']['value'])

    @property
    def id_feature(self):
        return self._id_feature

    @property
    def id(self):
        return self._id

    def getReference(self):
        return {'id': str(self._id_feature), 'id_feature_value': str(self._id)}
    @property
    def value(self):
        return self._value

    def text(self):
        return self._value.text()

class PSFeature:
    def __init__(self, raw):
        self._name = SimpleDescription.Translations().newDescription()
        self._values = {}

        p_feat = raw['product_feature']

        self._id = int(p_feat['id'])
        self._name.text(p_feat['name']['language']['value'])

    @property
    def id(self):
        return self._id

    def text(self):
        return self._name.text()

    def print(self):
        print(f"Feature: {self._name.text()}({self.id})")
        for k, v in self._values.items():
            # skip 'int' keys
            if isinstance(k, int):
                continue

            print(f"\t - {v.text()}('{k}')({v.id})")

    def getValue(self, key: str):
        return self._values[key]

    def getValue(self, my_id: int):
        return self._values[my_id]

    def addValue(self, f_value: PSFeatureValue):
        if self.id != f_value.id_feature:
            raise CallError(f"Value ({f_value.id}) not belong to this feature ({self.id})")

        key = URLFun.key_friendly_str(f_value.value.text())
        if key in self._values:
            raise CallError(f"Feature ({self.id}) value '{key}' already added")

        self._values[key] = f_value
        self._values[f_value.id] = f_value

    @staticmethod
    def getProductFeaturesList(raw):
        if not 'product_feature' in raw['product_features']:
            return []

        raw_features = raw['product_features']['product_feature']

        # just one element
        if isinstance(raw_features, dict):
            return [raw_features]

        return raw_features

    @staticmethod
    def getProductFeatureValuesList(raw):
        if not 'product_feature_value' in raw['product_feature_values']:
            return []

        raw_feat_vals = raw['product_feature_values']['product_feature_value']

        # if only one element is defined it can be not enclosed within list,
        # add the list around for iterations to work
        if isinstance(raw_feat_vals, dict):
            return [raw_feat_vals]

        return raw_feat_vals

