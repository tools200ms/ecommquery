# EcommQuery
Python e-commerce integration software.


## Loading configurations

Integration consists of a multiple configurations. 
Configuration is a configuration loaded from ini file (other formats possible in future) 
that contains one or multiple endpoints that can be of type: 

* PrestaShop API endpoint
* Web scrapping endpoint

Example code looks as follows: 
```python
from ecommquery import *
from ecommquery.core.loader_ini import IniLoader
from ecommquery.exceptions import EcommQueryError

try:
    inegr = Integrations()
    inegr.addLoaderAndRead(IniLoader('./configurations/PRODUCTION.ini'))
    inegr.addLoaderAndRead(IniLoader('./configurations/testing.ini'))

    inegr.print()
    
    do_stuff(inegr)
except EcommQueryError as ecq_err:
    print(ecq_err.message)
```
Output of `inegr.print()` might be following:
```
 INI file: ./configurations/PRODUCTION.ini (ini:PRODUCTION)
 Id # 0
     name: PrestaShop API
     host: https://www.example.com/grocerystore
 Id # 1
     name: PrestaShop API
     host: https://www.example.com/electronic-shop
 ==========================================================
 INI file: ./configurations/testing.ini (ini:testing)
 Id # 2
     name: PrestaShop API
     host: https://www.example.com/grocerystore-test01
 Id # 3
     name: PrestaShop API
     host: https://www.example.com/grocerystore-test02
 Id # 4
     name: PrestaShop API
     host: https://www.example.com/electronic-shop-test01
 Id # 5
     name: PrestaShop API
     host: https://www.example.com/electronic-shop-test02
 ====================================================
```
and the configuration files might look like bellow: 
```
# file: configurations/PRODUCTION.ini'))
[ecommquery]
memo = Production stores

[presta_api]
url = https://www.example.com/grocerystore
api_secret_key = TEST06LGUHL19KBQYMK8RNVU45ZK1C1Q

[presta_api]
url = https://www.example.com/electronic-shop
api_secret_key = ...

```

```
# file: configurations/testing.ini
[ecommquery]
memo = Testing setups

[presta_api]
url = https://www.example.com/grocerystore-test01
api_secret_key = ...

[presta_api]
url = https://www.example.com/grocerystore-test02
api_secret_key = ...

[presta_api]
url = https://www.example.com/electronic-shop-test01
api_secret_key = ...

[presta_api]
url = https://www.example.com/electronic-shop-test02
api_secret_key = ...
```

# Accessing service
Store products, manufacturers, taxes etc. can be accessed via 
service object that is created from endpoint using 
`.getService()` method:
```python
def do_stuff(inegr):
    ps = inegr.getService(endpoint='electronic-shop-test02')

    for prod_id in ps.getProductList():
        prod = ps.getProduct(prod_id)
        print(prod.name())
        print(prod.descr())

    the_prod = ps.getProduct('1012')

    the_prod.name('This is product\'s new name')
    # commit changes (update product at the store)
    ps.commitProduct(the_prod)
```

# References

* [PrestaShop 1.7 API](https://devdocs.prestashop-project.org/1.7/webservice/)
* [PrestaShop 8 API](https://devdocs.prestashop-project.org/8/webservice/)
* [Docker container with Prestashop tuned for development environment](https://hub.docker.com/r/200ms/prestashop_dev2)
