from .ecommquery import Integrations

from ecommquery.core.endpoint import Endpoint
from .lib import *

from .ext.filesystem.core.endpoint_fs import EndpointFS
from .ext.filesystem.core.endpoint_fs import ServiceFS
from .ext.filesystem.lib import *

# Import extensions:
from .ext.amazon_api0sp.core.endpoint_amsp import EndpointAmSP
from .ext.amazon_api0sp.core.endpoint_amsp import EndpointAmSP
from .ext.amazon_api0sp.lib import *

from .ext.prestashop_api.core.endpoint_ps import EndpointPS
from .ext.prestashop_api.core.endpoint_ps import ServicePS
from .ext.prestashop_api.lib import *

from .ext.web_scrap.core.endpoint_webscrap import EndpointWebScrap
from .ext.web_scrap.core.endpoint_webscrap import ServiceWebScrap
from .ext.web_scrap.lib import *

from .assistant.openai.core.endpointas_chatgpt import EndpointAsOpenAI
from .assistant.openai.core.endpointas_chatgpt import ServiceChatGPT
from .assistant.openai.lib import *
