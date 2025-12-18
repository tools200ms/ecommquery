import json
import os


class Stash:
    STASH_FILE = 'ecommquery_stash.json'

    def __init__(self, module: str, id: str):
        self._module = module
        self._id = id
        self._dom = None

    def load(self):
        with open(self.STASH_FILE, 'rw') as f:
            if not os.path.exists(self.STASH_FILE):
                # if empty create file:
                json.dump({self._module: {self._id: {}}}, f)
            else:
                obj = json.load(f)
                if not hasattr(obj, self._module):
                    obj[self._module] = {self._id: {}}
                    self._dom = {}
                else:
                    if not hasattr(obj[self._module], self._id):
                        obj[self._module][self._id] = {}
                        self._dom = {}
                    else:
                        self._dom = obj[self._module][self._id]

            json.dump(obj, f, indent=2)
        return

    def save(self):
        if self._dom == None:
            raise Exception('Stash has not been loaed')

        with open(self.STASH_FILE, 'rw') as f:
            obj = json.load(f)
            obj[self._module][self._id] = self._dom
            json.dump(obj, f, indent=2)

    def get(self, property):
        if self._dom == None:
            raise Exception('Stash has not been loaed')

        if not hasattr(self._dom, property):
            self._dom[property] = None

        return self._dom[property]

    def set(self, value):
        if self._dom == None:
            raise Exception('Stash has not been loaed')

        self._dom[property] = value
