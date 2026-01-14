import re
from pathlib import Path
import configparser

from ecommquery.core.endpoint import Endpoint
from ecommquery.core.loader import Loader
from ecommquery.exceptions import DataformatError


class IniLoader(Loader):
    def __init__(self, path = 'integrations.ini'):
        super().__init__()
        self.__path = Path(path).expanduser()


        self.__ini_parser = configparser.ConfigParser()
        with open(self.__path) as f:
            self.__ini_parser.read_file(f)

    def getInfo(self):
        return 'INI file: ' + str(self.__path);

    def genName(self):
        key = self.__path.name
        idx = key.lower().rfind('.ini')
        if idx > 0:
            key = key[0:idx]

        return 'ini:' + key

    def readConfig(self):
        try:
            sect = self.__ini_parser.sections()

            if sect[0] != 'ecommquery':
                raise DataformatError('Missing Heading [ecommquery] section')

            memo = self.__ini_parser.get(sect[0], 'memo')

            if self.__ini_parser.has_option(sect[0], 'name'):
                name = self.__ini_parser.get()
            else:
                name = self.genName()

            config = Loader.Config(memo, name)

            if len(sect[1:]) == 0:
                raise DataformatError('No configuration, only [ecommquery] section defined')

            for ep_name in sect[1:]:
                # Split by space or dot and take first part as ep_type
                ep_sect_split = re.split(r'[ .]', ep_name)
                ep_type = ep_sect_split[0]
                ep_id = ep_sect_split[1] if len(ep_sect_split) == 2 else None

                ep_class = Endpoint.getClass(ep_type)

                if ep_class is None:
                    raise DataformatError(f"Unknown endpoint '{ep_type}'")

                res = self.__ini_parser[ep_name]
                ep = ep_class(res, ep_id)
                    #.factory(self.__ini_parser[ep_type])
                config.addEndpoint(ep)

        except configparser.MissingSectionHeaderError as miss_sect_head_err:
            raise DataformatError('Missing section header')

        return config

    def save(self):
        pass
