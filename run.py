

from ecommquery import *
from ecommquery.core.loader_ini import IniLoader

from pprint import *

inegr = Integrations()
inegr.addLoaderAndRead( IniLoader('fs24-PROD.ini') )

inegr.print()

ps = inegr.getService()

prod = ps.getProduct('1184')

print(prod.name())

# v = ps.search('addresses', options={'limit': 10})

pprint( prod.images() )
pprint( prod.defImage() )
pprint( prod.getRaw()['product']['id_default_image'] )


prod.rmImage('4630')
prod.rmImage('4629')
prod.rmImage('4631')
prod.rmImage('4632')

print('RAW2:')
pprint( prod.images() )
pprint( prod.defImage() )
pprint(prod.getRaw()['product']['id_default_image'])

# ps.commitProduct(prod)
# ps.uploadImage('3-1.png', prod)
