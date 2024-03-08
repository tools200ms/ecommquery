

from ecommquery import *

from var_dump import var_dump
loader = IniLoader('fs24-PROD.ini')

inegr = Integrations()

inegr.addLoaderAndRead(loader)

inegr.list()

ps_srv = inegr.getService()

v = ps_srv.search('addresses', options={'limit': 10})

var_dump(v);

