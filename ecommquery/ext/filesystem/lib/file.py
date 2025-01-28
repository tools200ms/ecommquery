from pathlib import Path

from ecommquery.lib.file import File

class FSFile (File):
    def __init__(self, file):
        self._file = file
        self._path = Path(file.name)

    # TODO: add close() operation
    @property
    def content(self):
        return self._file.read()

    @property
    def file_name(self):
        return self._path.name

    @property
    def file_size(self):
        return self._path.stat().st_size

    @property
    def creation_time(self):
        return self._path.stat().st_ctime

    @property
    def modification_time(self):
        return self._path.stat().st_mtime


