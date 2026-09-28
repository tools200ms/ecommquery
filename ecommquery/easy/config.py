import os

from ecommquery.core.loader_ini import IniLoader
from ecommquery import Integrations


class Config:
    @staticmethod
    def load(path: str = None) -> Integrations:
        path = path or (os.getenv('APP_ROOT', '/app') + '/conf')

        integr = Integrations()

        if os.path.isfile(path):
            integr.addLoaderAndRead(IniLoader(path))
        elif os.path.isdir(path):
            for ini_file in (f for f in os.listdir(path) if f.endswith('.ini')):
                integr.addLoaderAndRead(IniLoader(os.path.join(path, ini_file)))
        else:
            raise FileNotFoundError(f"The specified path '{path}' is neither a valid file nor a directory.")

        integr.print()

        return integr
