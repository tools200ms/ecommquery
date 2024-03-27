
from ecommquery import *
from ecommquery.core.loader_ini import IniLoader

from pprint import *

inegr = Integrations()
inegr.addLoaderAndRead( IniLoader('fs24-PROD.ini') )

inegr.print()

ps = inegr.getService( 0, 'presta_api' )

wps = inegr.getService( 0, 'wp_scrap' )
prod_s = wps.getProduct('')


s_prod_name = prod_s.name()
s_prod_descr = prod_s.description()

prod_t = ps.getProduct( '1192' )

prod_t.name(s_prod_name)
prod_t.description('<p>' + s_prod_descr + '</p>' + prod_t.description() )


# validators bs4

# v = ps.search('addresses', options={'limit': 10})

#pprint( prod.images() )
#pprint( prod.defImage() )
#pprint( prod.getRaw()['product']['id_default_image'] )


#prod.rmImage('4630')
#prod.rmImage('4629')
#prod.rmImage('4631')
#prod.rmImage('4632')

#print('RAW2:')
#pprint( prod.images() )
#pprint( prod.defImage() )
#pprint( prod.getRaw()['product']['id_default_image'] )

ps.commitProduct(prod_t)
# ps.uploadImage('3-1.png', prod)
