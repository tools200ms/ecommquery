

from ecommquery import *
from ecommquery.core.loader_ini import IniLoader

from var_dump import var_dump

inegr = Integrations()
inegr.addLoaderAndRead( IniLoader('fs24-PROD.ini') )

inegr.print()

ps_srv = inegr.getService()

prod = ps_srv.getProduct('1184')

print(prod.name())

v = ps_srv.search('addresses', options={'limit': 10})

var_dump(v);

