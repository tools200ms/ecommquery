import configparser

from ecommquery.core.loader import Loader, LoaderParserError
from ecommquery.core.endpoint import Endpoint

class IniLoader(Loader):
    def __init__(self, path = 'integrations.ini'):
        super().__init__()
        self.__path = path;
        self.__ini_parser = configparser.ConfigParser()
        self.__ini_parser.read(path)

    def getInfo(self):
        return 'INI file: ' + self.__path;

    def readConfig(self):
        try:
            sect = self.__ini_parser.sections()

            if sect[0] != 'ecommquery':
                raise LoaderParserError('Missing Heading [ecommquery] section')

            memo = self.__ini_parser.get(sect[0], 'memo')
            config = Loader.Config(memo)

            for ep_type in sect[1:]:

                ep_class = Endpoint.getClass(ep_type)

                if ep_class == None:
                    raise LoaderParserError('Unknown endpoint \'' + '\'')

                ep = ep_class.factory( self.__ini_parser[ep_type] )
                config.addEndpoint( ep )

        except configparser.MissingSectionHeaderError as miss_sect_head_err:
            raise LoaderParserError('Missing section header')

        return config

    def save(self):
        pass
