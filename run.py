

from ecommquery import *

from var_dump import var_dump

inegr = Integrations( 'fs24-test.ini' ).load()

inegr.list()

ps_srv = inegr.getService()

v = ps_srv.search('addresses', options={'limit': 10})

var_dump(v);

