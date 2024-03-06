
from . import ini_config

class IniConfig:
    def __init__( self, file_path ):
        self.file_path = file_path

    def load(self):
        self.config = ini_config.read( self.file_path )

        return self.config

    def save(self):
        pass

