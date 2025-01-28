from typing import Final

from ecommquery import Endpoint
from ecommquery.assistant.lib.query_loader import QueryLoader
from ecommquery.assistant.openai.core.service_chatgpt import ServiceChatGPT
from ecommquery.core.validators import RegExValidator, ListValidator, PathValidator
from ecommquery.ecommquery import Mode


class EndpointAsOpenAI(Endpoint):

    model_versions: Final = (
        # GPT-4 Family
        "gpt-4",              # Standard GPT-4 model with full capabilities, high accuracy.
        "gpt-4-turbo",        # Optimized version of GPT-4; faster and cheaper.

        # GPT-3.5 Family
        "gpt-3.5",            # Standard GPT-3.5 model; less capable than GPT-4 but effective.
        "gpt-3.5-turbo",      # Optimized version of GPT-3.5; faster and more cost-efficient.

        # Codex Family (For Code Completion Tasks)
        "code-davinci-002",   # Advanced code generation model, high accuracy for coding tasks.
        "code-cushman-001",   # Lightweight code completion model, faster but less powerful.

        # Embedding Models
        "text-embedding-ada-002",  # Embedding model for search, similarity, and NLP tasks.

        # Moderation Models
        "moderation-latest"   # Model for content moderation tasks; ensures safe usage.
    )

    @staticmethod
    def reg_name():
        return 'chatgpt'

    @staticmethod
    def name():
        return "OpenAI ChatGPT API"

    def __init__(self, params: {}):
        super().__init__( {'version': Endpoint.Constr(
                                    ListValidator( EndpointAsOpenAI.model_versions, 0) ),
                           'key': Endpoint.Constr(
                                        # don't do to strict validation, if API provider would
                                        # decide to support longer keys, or extend it by a low casec haracter cases
                                        # characters (assuming that UPPER case characters are curently used)
                                        # this code sould handle change without updates.
                                        # Exact validation is made by library that talks to API
                                        RegExValidator('[a-zA-Z0-9|-|_]{16,96}')),
                           'queries': Endpoint.Constr(PathValidator('queries'),
                                re_name = 'queries_path')
                                    },
                         params )

    def info(self):
        return "Model version: " + self._version

    def _getService(self, mode: Mode):
        q_loader = QueryLoader(self._queries_path)

        return ServiceChatGPT(self._key, self._version, q_loader.getQueries(), **(Mode.as_args(mode)))

Endpoint.register(EndpointAsOpenAI)
