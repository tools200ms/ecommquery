import json
import os
from pathlib import Path

class Stash:
    STASH_DEFAULT_FILE = 'ecommquery_stash.json'

    def __init__(self, module: str, id: str, stash_file: Path = Path(STASH_DEFAULT_FILE)):
        self._module = module
        self._id = id
        self._stash_file = stash_file
        self._dom = None

    def _load(self):
        pass
    
    def load(self):
        if (     not os.path.exists(self._stash_file) or 
                (self._stash_file.is_file() and self._stash_file.stat().st_size == 0)):
            # if empty create file:
            with open(self._stash_file, 'w') as file:
                json.dump({self._module: {self._id: {}}}, file, indent=2)
            self._dom = {}
            return

        # Check if _stash_file is a file type
        if not self._stash_file.is_file():
            raise Exception(f"Stash file path is not a file: {self._stash_file}")

        # else
        with open(self._stash_file, 'r+') as file:
            file.seek(0)
            obj = json.load(file)
            if self._module not in obj or self._id not in obj[self._module]:
                obj[self._module] = {self._id: {}}
                file.seek(0)
                json.dump(obj, file, indent=2)
                self._dom = {}
                return

        self._dom = obj[self._module][self._id]
        # end of load

    def set(self, prop, value):
        if self._dom == None:
            raise Exception('Stash has not been loaed')
        self._dom[prop] = value

    def get(self, property):
        if self._dom == None:
            raise Exception('Stash has not been loaed')

        return self._dom[property]

    def save(self):
        if self._dom == None:
            raise Exception('Stash has not been loaed')

        with open(self._stash_file, 'w+') as file:
            file.seek(0)
            obj = json.load(file)
            obj[self._module][self._id] = self._dom
            file.seek(0)
            json.dump(obj, file, indent=2)

