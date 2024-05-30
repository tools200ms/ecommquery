# EcommQuery

Python e-commerce integration framework. This project has been 
developed to handle automation tasks for eCommerce. 

Its concept is based on endpoints that can be of type: 
- **Data source**
- or **AI assistant**

User defines the **Task** that is a Python code calling appropriately endpoints to do a desired job in eCommerce system.

EcomQuery operates on: 
- product data (name, description, ...) and metadata (weight, codes, ...)
- and product related data (categories, brands, ...) and its metadata (category index, ...)

**Data source** is an end that allows on product and product related data access. One of the data sources is PrestaShop API. 

**AI assistant** is an interface for prompting AI (such as OpenAI's ChatGPT) with purpose of doing a certain operations on product or product related data. It could be for instance data extraction (e.g. to place product in desired categories), or improvement of description quality.

The framework provides common (regardless of eCommerce at the backend) interface for accessing product and other data. 
EcomQuery operates in 'language context'. Textual data such as names, descriptions must be linked with a language that are written in. It means also that one text can hold multiple language versions. This is to cover multilingual shops.

# Configuration
ECommQuery endpoints have to be configured by parameters, bellow the list of endpoints and its parameters:

Data Source: 
* `presta_api`- PrestaShop API endpoint
  * *url* - store or API URL
  * *api_secret_key* - API key
* `web_scrap`- Web scrapping endpoint
  * *url* - store URL

AI assistant:
* `chatgpt`- ChatGPT
  * *version* - model version, default: `gpt-3.5-turbo`
  * *key* - ChatGPT key
  * *queries* - path to directory with prompt files (see )

## Configuration files
Configuration is hold in ini file, the format is: 
```
[ecommquery]
memo = <Description of what is in this config.>

# Endpoint, e.g.:
[presta_api]
memo = <optional description>
url = https://www.example.com/grocerystore
api_secret_key = TEST06LGUHL19KBQYMK8RNVU45ZK1C1Q

[web_scrap]
memo = <optional description>
url = https://example.com/store
```

## Propmpt files
User defines AI prompts in Machine/Model Prompt (*.mp.txt) file, simple example: 
```
@lookup_for_categories product
Please lookup of categories of the product 
of which description is below: 
=== Description Begin ===
{product.descr}
=== Description End ===

Return your responce in JSON foramt.
@end

# next prompt definitins ...
```
Content between `@lookup_for_categories` and `@end` sections is a prompt message.

`@lookup_for_categories` is a prompt name, followed by a class name of the object that is to be datasource for prompt.
In this case `{product.descr}` inserts Product's description into prompt message.

# Usage Examples
User defines tasks that operate on endpoints to achieve desired results.
Bellow are an example code scraps demonstrating usage.

## Loading configurations

Starting point is `Integrations` object that is used for loading configurations. One configuration file might hold multiple endpoints. There might be one or more configuration files that can be loaded into 'Integration', see example:
```python
from ecommquery import *
from ecommquery.core.loader_ini import IniLoader
from ecommquery.exceptions import EcommQueryError

try:
    inegr = Integrations()
    inegr.addLoaderAndRead(IniLoader('./configurations/testing-noe.ini'))
    inegr.addLoaderAndRead(IniLoader('./configurations/testing-sim.ini'))

    inegr.print()
    
    do_stuff(inegr)
except EcommQueryError as ecq_err:
    print(ecq_err.message)
```
Output of `inegr.print()` might be following:
```
 INI file: ./configurations/testing-noe.ini (ini:PRODUCTION)
 Id # 0
     name: PrestaShop API
     host: https://noe-test.example.com/grocerystore
 Id # 1
     name: PrestaShop API
     host: https://noe-test.example.com/electronic-shop
 ==========================================================
 INI file: ./configurations/testing-sim.ini (ini:testing)
 Id # 2
     name: PrestaShop API
     host: https://sim-test.example.com/grocerystore-test01
 ====================================================
```
and the configuration files might look like bellow: 
```
# file: configurations/testing-noe.ini'))
[ecommquery]
memo = Testing stores @ Noe

[presta_api]
url = https://noe-test.example.com/grocerystore
api_secret_key = TEST06LGUHL19KBQYMK8RNVU45ZK1C1Q

[presta_api 2]
url = https://noe-test.example.com/electronic-shop
api_secret_key = ...

```
and 
```
# file: configurations/testing.ini
[ecommquery]
memo = Testing setups @ Sim

[presta_api]
url = https://sim-test.example.com/grocerystore-test01
api_secret_key = ...
```

Once configuration is loaded task is ready for accessing resources.

## Accessing service
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

## HTML sterilisation
While working for custommers I found a common issue that HTML descriptions hold leftovers from data migration from a previus system. For instance, HTML code can contain 'div' elemets having defined classes that are nonexistent in a new system, or have 'img' elements with urls pointing to an old system.

Therefore, code sterilisation is a vital part of migration process.
Function `HTMLfun.sanitize(html: str)` cleansup code as follows: 
* unwrap (remove tag keeping its content) all elements that are **not**: 
  * `h1`, `h2`, `h3`, `h4`, `h5`, `h6` - header tags
  * `p`, `br` - format tags
  * `b`, `i`, `strong`, `em`, `u` - style tags
  * `table`, `tbody`, `th`, `tr`, `td` - table tags
  * `ul`, `ol`, `li` - list tags
  
  Note that `div` and `span` elements are also removed (unwraped).
* `h1` element is kind of special, only one `h1` element should be defined on page. In templates used by eCommerce platforms `h1` is usually a product or category name. It is a good idea from SEO point of view. It means also that when sterilizing description any encounted `h1` tags should be shifted to become `h2`. Argument `start_hlevel=2` forces all `Header` elements to start from `h2`. 
* remove empty **style** elements, such as `<b></b>`
* merge consecutive style elements, for instance `<b>B</b><b>old</b>` merges to `<b>Bold</b>`. 
  This it to eliminate an over definition. I found that this can exist surprisingly often.
* purge `style` or `class` tag arguments if argument: 
  `purge_classes = True` or `purge_styles = True` is provided.

When sterilized HTML code is translated to plain text it looks better (no muliple new lines, no strange spaces).
Plain text is a way to communicate with AI, thus machine recives well formatted text. For instance, while translating unsterilized `<b>Co</b><b>conut</b>` to text the output is `Co conut`, thus tag merging is kind important.

# Implementation status

Data source for Product: 

| Function                       | PrestaShop API | Web scrap |
|--------------------------------|----------------|-----------|
| *Product data*                 |                |           |
| name                           | [x]            | [x]       |
| short description              |                |           |
| description                    |                |           |
| price                          |                |           |
| available stock                |                |           |
| *codes*                        |                |           |
| EAN                            |                |           |
| MPN (manufacturer part number) |                |           |
| Id (platform specific code)    |                |           |
| *shipping data*                |                |           |
| weight                         |                |           |
| dimensions (W*H*D)             |                |           |

Data source for Categories:

| Function    | PrestaShop API | Web scrap |
|-------------|----------------|-----------|
| name        |                |           |
| description |                |           |

Data source for Brands:

| Function    | PrestaShop API | Web scrap |
|-------------|----------------|-----------|
| name        |                |           |
| description |                |           |

# References

* [PrestaShop 1.7 API](https://devdocs.prestashop-project.org/1.7/webservice/)
* [PrestaShop 8 API](https://devdocs.prestashop-project.org/8/webservice/)
* [Docker container with Prestashop tuned for development environment](https://hub.docker.com/r/200ms/prestashop_dev2)
* [OpenAI API reference](https://platform.openai.com/docs/api-reference)
