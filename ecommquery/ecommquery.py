# integrations source
class Integrations:
    class LoadedConf:
        def __init__(self, loader, conf):
            self.loader = loader
            self.conf = conf
    def __init__( self ):
        self.__inte = []

    def addLoaderAndRead(self, loader):
        self.__inte.append(Integrations.LoadedConf(loader, loader.readConfig()))

    def print(self):
        if len(self.__inte) == 0:
            print( "No integrations has been loaded" )
            return

        for inte in self.__inte:
            loader_info = inte.loader.getInfo()
            print( ' ' + loader_info + ' (' + ')' )

            for e in inte.conf.endpoints():
                print(' Id # %s' % ( e.id() ) )
                print(' %sname: %s' % ( 4 * ' ', e.name() ) )
                print(' %shost: %s' % ( 4 * ' ', e.info() ) )

            print( ' ' + (len(loader_info) * '=') )


    def getService(self, c_id = 0, e_id = None):
        if e_id == None:
            e_no = self.__inte[c_id].conf.endpointNo()
            if e_no == 1:
                ep = self.__inte[c_id].conf.endpoint()
            elif e_no == 0:
                raise Exception('Empty Endpoint configuration')
            else:
                raise Exception('Multiple endpoints, specify which one to use')
        else:
            ep = self.__inte[c_id].conf.endpoint(e_id)

        return ep.getService()

class ECommDef:
    class Unset:
        pass
