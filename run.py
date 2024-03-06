
from prestapyt import PrestaShopWebService
from ecommquery import IniConfig

from var_dump import var_dump

config = IniConfig( 'fs24-test.ini' ).load()

print(config.memo)
#prestashop = PrestaShopWebService('https://test.foodieshop24.pl/api', '6PMBR6LGUHL19KBQYMK8RNVU45ZK1C1Q', verbose=True)

#v = prestashop.search('addresses', options={'limit': 10})

#var_dump(v);

