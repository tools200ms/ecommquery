# EcommQuery

AI integration framework for e-commerce. The project's aim is to provide a tool to automate eCommerce tasks with AI. 

Its concept is based on endpoints that can be of type:
- **Data source** is an endpoint allowing product and product related data access. One of the data sources is PrestaShop API.
- **AI assistant** is an interface for prompting AI (such as OpenAI's ChatGPT) with purpose of doing a certain operations on product or product related data.

EcommQuery uses a simple self-explaing prompt file format: 
```
# file: product.prompt.txt

@generate_short_descr_of product
Below text is a description of a product:
=== Text Begin ===
{product.descr}
=== Text End ===

Generate short description, return only generated short description in a plain text.
```

## Usage
To use the framework: 
- configure endpoints
- develop prompt
- develop 'task'
- test and run

### Configuration files - configuring endpoints
The configuration is stored in an INI file: 
```
[ecommquery]
memo = <Explanation of the contents of this configuration.>

# Endpoint for accessing PrestaShop:
[presta_api]
memo = <optional description>
url = https://www.example.com/grocerystore
api_secret_key = TEST06LGUHL19KBQYMK8RNVU45ZK1C1Q

# Endpoint for accessing OpenAI's ChatGPT
[chatgpt]
memo = Chat GPT assistant API
key = DUMMY_KEY-ohsazaejou83d
queries = ~/prompts/
```
### Prompt file format
Line `queries = ~/prompts/` indicates where prompt files are located. User defines AI prompts in Machine/Model Prompt (*.mp.txt) file, simple example: 
```
@assign_cat_for product
Can you determine categories that fit to the 
following product description?:
=== Description Begin ===
{product.name}
{product.cdescr}
=== Description End ===

Aim to find one or maximum three best categories. Categories are
limited to the names from the list below:
... THE LIST ...
.... .... ....

Format output as JSON array.
@end

# next prompt definitins ...
```
Content between `@assign_cat_for` and `@end` sections is a prompt message.

`@assign_cat_for` is a prompt name, followed by a class name of the object that is to be datasource for prompt.
In this case `{product.descr}` inserts Product's description into a prompt message.

### Developing tasks
Let's develop a task that will assign product categories based on AI prompt response: 

```python
from ecommquery import *
from ecommquery.core.loader_ini import IniLoader
from ecommquery.exceptions import EcommQueryError

try:
    integr = Integrations()
    integr.addLoaderAndRead(IniLoader('./config.ini'))

    ps = inegr.getService(endpoint='prestashop')
    ai = inegr.getService(endpoint='chatgpt')

    for prod_id in ps.getProductList():
        prod = ps.getProduct(prod_id)
        
        res = ai.sendPrompt('assign_cat_for', [prod])
        
        prod.addCat(json.loads(res))
        ps.commitProduct(the_prod)

    ai.close()
    ps.close()
except EcommQueryError as ecq_err:
    print(ecq_err.message)
```

# Implemented endpoints
Below is the list of supported endpoints and its parameters: 

Data Source: 
* `presta_api`– PrestaShop API endpoint
  * *url* – store or API URL
  * *api_secret_key* – API key
* `allegro_api`– Allegro API
  * *client_id* – client ID
  * *client_secret* – client secret
  * *sandbox* – sandbox mode, default: `False`
* `web_scrap`– Web scrapping endpoint
  * *url* – store URL

AI assistant:
* `chatgpt`- ChatGPT
  * *version* - model version, default: `gpt-3.5-turbo`
  * *key* – ChatGPT key
  * *queries* – path to directory with prompt files (see [example/prompts](./example/prompts))

# Detailed usage
`Integrations()` object can be used to load more than one configuration file. In such a case, configurations are merged. Look at an example below: 

INI file `configurations/testing-noe.ini`: 
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
INI file `configurations/testing-sim.ini`: 
```
# file: configurations/testing-sim.ini
[ecommquery]
memo = Testing setups @ Sim

[presta_api]
url = https://sim-test.example.com/grocerystore-test01
api_secret_key = ...
```

Python code: 
```python
from ecommquery import *
from ecommquery.core.loader_ini import IniLoader
from ecommquery.exceptions import EcommQueryError

try:
    integr = Integrations()
    integr.addLoaderAndRead(IniLoader('./configurations/testing-noe.ini'))
    integr.addLoaderAndRead(IniLoader('./configurations/testing-sim.ini'))

    # print 
    integr.print()
    
    do_stuff(integr)
except EcommQueryError as ecq_err:
    print(ecq_err.message)
```
Output of `inegr.print()` is following:
```
 INI file: ./configurations/testing-noe.ini (ini:PRODUCTION)
 Id #0
     name: PrestaShop API
     host: https://noe-test.example.com/grocerystore
 Id #1
     name: PrestaShop API
     host: https://noe-test.example.com/electronic-shop
 ==========================================================
 INI file: ./configurations/testing-sim.ini (ini:testing)
 Id #2
     name: PrestaShop API
     host: https://sim-test.example.com/grocerystore-test01
 ====================================================
```

## Accessing service
Store products, manufacturers, taxes, etc. can be accessed via 
a service object created by endpoint with 
`.getService()` method:
```python
def do_stuff(inegr):
    ps = inegr.getService(endpoint='electronic-shop-test02')

    for prod_id in ps.getProductList():
        prod = ps.getProduct(prod_id)
        print(prod.name)
        print(prod.descr)

    the_prod = ps.getProduct('1012')

    the_prod.name('This is product\'s new name')
    # commit changes (update product at the store)
    ps.commitProduct(the_prod)
```

## HTML sterilisation
When processing HTML data, 'sterilization' is a good practice to ensure that there are not any 'meaningless' tags or attributes.

Function `HTMLfun.sanitize(html: str)` provided by eCommQuery cleans up HTML as follows: 
* unwrap (remove tag keeping its content) all elements that are **not**: 
  * `h1`, `h2`, `h3`, `h4`, `h5`, `h6` - header tags
  * `p`, `br` - format tags
  * `b`, `i`, `strong`, `em`, `u` - style tags
  * `table`, `tbody`, `th`, `tr`, `td` - table tags
  * `ul`, `ol`, `li` - list tags
  
  Note that `div` and `span` elements are also removed (unwraped).
* `h1` element is kind of special, only one `h1` element should be defined on page. In templates used by eCommerce platforms `h1` is usually a product or category name. It is a good idea from an SEO point of view. It means also that when sterilizing description any encounted `h1` tags should be shifted to become `h2`. Argument `start_hlevel=2` forces all `Header` elements to start from `h2`. 
* remove empty **style** elements, such as `<b></b>`
* merge consecutive style elements, for instance `<b>B</b><b>old</b>` merges to `<b>Bold</b>`. 
  This is to eliminate an over definition. I found that this can exist surprisingly often.
* purge `style` or `class` tag arguments if argument: 
  `purge_classes = True` or `purge_styles = True` is provided.

When sterilized HTML code is translated to plain text, it looks better (no multiple new lines, no strange spaces).
Plain text is a way to communicate with AI, thus machine receives well-formatted text. For instance, while translating unsterilized `<b>Co</b><b>conut</b>` to text the output is `Co conut`, thus tag merging is kind important.

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


# Troubleshooting

The fastest way to diagnose issues is to change framework's mode.

## Modes
The Framework provides the following modes: 

- Mode.WORK, normal operation, no output messages, only if print( ... ) function is called from a task.
- Mode.DEBUG, print a lot of detailed messages, including those from modules used by framework (`prestapyt`, `openai`).
- Mode.VERBOSE, print only `ecommquery` related messages (no output messages from modules).
- Mode.PRETEND, 'dry run', do not change the system's state:
  - for **Data source** any read operation is performed normally, while modificatins are skiped - system prints only message what would be done.
  - for **AI assistant** prompts are not sent to AI but simply print.

Mode can be passed to `Integrations` object: 
```python
inegr = Integrations( Mode.DEBUG )
```
in this case the `Mode.DEBUG` will apply to all endpoints. Mode can be also set only for a certain 'problematic' endpoint: 
```python
endpoint = inegr.getService( mode = Mode.DEBUG, endpoint = 'presta_api' )
```

Modes can be combined: 
```python
inegr = Integrations( Mode.VERBOSE | Mode.PRETEND )
```
In above case framework will pretend that is "doing changes" but also be "verbosable".

## Known issues

`prestapyt` requires `packaging` module, but it is not automatically pulled, if you see: 
> ModuleNotFoundError: No module named 'distutils'

and Python version is `>= 3.12`, install `packaging` module, it solves the issue.

# References

* [PrestaShop 1.7 API](https://devdocs.prestashop-project.org/1.7/webservice/)
* [PrestaShop 8 API](https://devdocs.prestashop-project.org/8/webservice/)
* [Python PrestaShop API access module](https://github.com/prestapyt/prestapyt)
* [PrestaShop API access Pyton module - Prestapyt](https://github.com/prestapyt/prestapyt)
* [Docker container with Prestashop tuned for development environment](https://hub.docker.com/r/200ms/prestashop_dev2)
* [OpenAI API reference](https://platform.openai.com/docs/api-reference)
* [Amazon SP API samples](https://github.com/amzn/selling-partner-api-samples/tree/main)
* [Allegro REST API](https://developer.allegro.pl/tutorials/uwierzytelnianie-i-autoryzacja-zlq9e75GdIR)

