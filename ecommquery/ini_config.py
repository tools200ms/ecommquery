import configparser

from .config import *

class ECQParserError(Exception):
    pass


def read( path ):
    ini_parser = configparser.ConfigParser()

    try:
        ini_parser.read( path )

        sect = ini_parser.sections()

        if sect[0] != 'ecommquery':
            raise ECQParserError( 'Missing Heading [ecommquery] section' )

        memo = ini_parser.get(sect[0], 'memo')
        config = Config(memo)

        for s in sect[1:] :
            match s:
                case 'presta':
                    if ini_parser.has_option( s, 'memo' ):
                        c = ConfigPS(ini_parser.get(s, 'url'), ini_parser.get(s, 'api_secret_key'), ini_parser.get(s, 'memo') )
                    else:
                        c = ConfigPS(ini_parser.get( s, 'url' ), ini_parser.get( s, 'api_secret_key' ), None)
                    config.add(c)
                case _:
                    print ('Unknown section ' + s + ', ignorring');


    except configparser.MissingSectionHeaderError as miss_sect_head_err:
        raise ECQParserError('Missing section header')

    return config
