import os.path
import configparser

from ecommquery.core.endpoint import Endpoint
from ecommquery.core.loader import Loader
from ecommquery.exceptions import DataformatError


class IniLoader(Loader):
    def __init__(self, path = 'integrations.ini'):
        super().__init__()
        self.__path = path;
        self.__ini_parser = configparser.ConfigParser()
        self.__ini_parser.read(path)

    def getInfo(self):
        return 'INI file: ' + self.__path;

    def genName(self):
        key = os.path.basename(self.__path)
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

            for ep_type in sect[1:]:

                ep_class = Endpoint.getClass(ep_type)

                if ep_class == None:
                    raise DataformatError('Unknown endpoint \'' + '\'')

                ep = ep_class.factory( self.__ini_parser[ep_type] )
                config.addEndpoint( ep )

        except configparser.MissingSectionHeaderError as miss_sect_head_err:
            raise DataformatError('Missing section header')

        return config

    def save(self):
        pass
