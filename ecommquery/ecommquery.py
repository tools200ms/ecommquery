# integrations source
from ecommquery.exceptions import CallError


class Integrations:
    class LoadedConf:
        def __init__(self, loader, conf):
            self.loader = loader
            self.conf = conf
    def __init__( self ):
        self.__inte = {}

    def addLoaderAndRead(self, loader):
        conf = loader.readConfig()
        conf_key = conf.getName()

        # add postfix in the case of key name collision
        if conf_key in self.__inte:
            conf_key2 = None
            for idx in range(1,15):
                conf_key2 = conf_key + ("-%x" % idx)
                if conf_key2 not in self.__inte:
                    break
            if conf_key2 == None:
                raise CallError('key name collision: ' + conf_key)
            conf_key = conf_key2

        integration = Integrations.LoadedConf(loader, conf)
        self.__inte[conf_key] = integration

        return integration

    def print(self):
        if len(self.__inte) == 0:
            print( "No integrations has been loaded" )
            return

        for conf_key, inte in self.__inte.items():
            inte_msg = ' ' + inte.loader.getInfo() + ' (' + conf_key + ')'
            print(inte_msg)

            for e in inte.conf.endpoints():
                print(' Id # %s' % ( e.id() ) )
                print(' %sname: %s' % ( 4 * ' ', e.name() ) )
                print(' %shost: %s' % ( 4 * ' ', e.info() ) )

            print( ' ' + (len(inte_msg) * '=') )


    def getService(self, conf_id = None, ep_id: str = None, endpoint = None):
        ep = None

        if len(self.__inte) == 0:
            raise CallError('Empty configuration')

        if conf_id == None and len(self.__inte) == 1:
            conf_id = list(self.__inte.keys())[0]
        elif conf_id == None: # search for endpoint
            for inet in self.__inte.values():
                ep_match = inet.conf.endpoint(id = ep_id, pattern = endpoint)
                if ep_match != None and ep == None:
                    ep = ep_match
                elif ep_match != None:
                    raise CallError('Ambiguous endpoint references')

            if ep == None:
                raise CallError('No endpoint has been found')

            return ep.getService()

        # pick endpoint
        if conf_id not in self.__inte:
            raise CallError('Conf.Id has not been found: ' + conf_id)

        ep = self.__inte[conf_id].conf.endpoint(endpoint)

        return ep.getService()

class ECommDef:
    class Unset:
        pass
