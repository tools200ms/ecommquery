import json
import os
from datetime import datetime
from pathlib import Path

class Stash:
    STASH_DEFAULT_FILE = 'ecommquery_stash.json'
    _cache = None
    _mod_time = None
    _register = set()

    def __init__(self, module: str, id: str, stash_file: Path = Path(STASH_DEFAULT_FILE)):
        self._module = module
        self._id = id
        self._stash_file = stash_file
        self._dom = None

        self._modid = module + ':' + id

        if self._modid in Stash._register:
            raise Exception(f"Stash with module '{module}' and id '{id}' already exists")

        Stash._register.add(self._modid)

    def close(self):
        self._module = None
        self._id = None
        self._stash_file = None
        self._dom = None
        Stash._register.remove(self._modid)

    def load(self):
        if (     not os.path.exists(self._stash_file) or 
                (self._stash_file.is_file() and self._stash_file.stat().st_size == 0)):
            # if empty create file:
            with open(self._stash_file, 'w') as file:
                Stash._cache = {self._module: {self._id: {}}}
                json.dump(Stash._cache, file, indent=2)
            self._dom = {}
            return

        # Check if _stash_file is a file type
        if not self._stash_file.is_file():
            raise Exception(f"Stash file path is not a file: {self._stash_file}")

        if Stash._mod_time == None or Stash._mod_time != self._stash_file.stat().st_mtime:
            with open(self._stash_file, 'r+') as file:
                file.seek(0)
                Stash._cache = json.load(file)
                Stash._mod_time = self._stash_file.stat().st_mtime
                if self._module not in Stash._cache or self._id not in Stash._cache[self._module]:
                    Stash._cache[self._module] = {self._id: {}}
                    file.seek(0)
                    json.dump(Stash._cache, file, indent=2)
                    self._dom = {}
                    return

        self._dom = Stash._cache[self._module][self._id].copy()
        print(self._dom)
        # end of load

    def set(self, prop, value):
        if self._dom == None:
            raise Exception('Stash has not been loaed')
        self._dom[prop] = value

    def setDate(self, prop, date:datetime):
        if date == None:
            self.set(prop, None)
        else:
            self.set(prop, date.strftime('%Y-%m-%d %H:%M:%S'))

    def unset(self, prop):
        if self._dom == None:
            raise Exception('Stash has not been loaed')
        del self._dom[prop]

    def get(self, prop):
        if self._dom == None:
            raise Exception('Stash has not been loaed')

        if not prop in self._dom:
            return None

        return self._dom[prop]

    def getDate(self, prop)-> datetime:
        return datetime.strptime(self.get(prop), '%Y-%m-%d %H:%M:%S')

    def save(self):
        if self._dom == None:
            raise Exception('Stash has not been loaed')

        with open(self._stash_file, 'w') as file:
            Stash._cache[self._module][self._id] = self._dom
            json.dump(Stash._cache, file, indent=2)

