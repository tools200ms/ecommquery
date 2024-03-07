
from . import ini_config

# integrations source
class Integrations:
    def __init__( self, file_path ):
        self.file_path = file_path

    def load(self):
        self.config = ini_config.read( self.file_path )

        return self

    def save(self):
        pass

    def list(self):
        if self.config == None:
            print( "No configuration has been loaded" )
            return

        for inte in self.config.integrations():
            print('Id # %s' % ( inte.id() ) )
            print('%sname: %s' % ( 4 * ' ', inte.endPoint() ) )
            print('%shost: %s' % ( 4 * ' ', inte.info() ) )


    def getService(self, id = None):
        if id == None and len( self.config.configs ) == 1:
            index = 0
        elif id == None:
            raise Exception( 'Multiple services, specify which one to provide' )

        return self.config.configs[index].getService()
