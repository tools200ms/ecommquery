from typing import Final

from ecommquery import Endpoint
from ecommquery.assistant.lib.query_loader import QueryLoader
from ecommquery.assistant.openai.core.service_chatgpt import ServiceChatGPT
from ecommquery.core.validators import RegExValidator, ListValidator, PathValidator
from ecommquery.ecommquery import Mode


class EndpointAsOpenAI(Endpoint):

    model_versions: Final = (
        # GPT-5.6 Family
        "gpt-5.6-sol",
        "gpt-5.6-terra",
        "gpt-5.6-luna",

        # GPT-5 Family
        "gpt-5",
        "gpt-5-pro",
        "gpt-5-mini",
        "gpt-5-nano",
        # GPT / Reasoning / Chat (code & general text)
        "gpt-4o",  # flagship multimodal/general model
        "gpt-4o-mini",  # faster/cheaper general model

        # (Optional) If you want separate “reasoning” models too
        # "o1",
        # "o3",

        # Embeddings (replacement for text-embedding-ada-002)
        "text-embedding-3-small",
        "text-embedding-3-large",

        # Moderation
        "text-moderation-latest",
        "text-moderation-stable",
    )

    @staticmethod
    def reg_name():
        return 'chatgpt'

    @staticmethod
    def name():
        return "OpenAI ChatGPT API"

    def __init__(self, params: {}, id:str):
        super().__init__( {'version': Endpoint.Constr(
                                    ListValidator( EndpointAsOpenAI.model_versions, 0) ),
                           'key': Endpoint.Constr(
                                        # don't do to strict validation, if API provider would
                                        # decide to support longer keys, or extend it by a low casec haracter cases
                                        # characters (assuming that UPPER case characters are curently used)
                                        # this code sould handle change without updates.
                                        # Exact validation is made by library that talks to API
                                        RegExValidator('[-|_|a-zA-Z0-9]{64,256}')),
                           'queries': Endpoint.Constr(PathValidator('queries'),
                                alt_name = 'queries_path')
                                    },
                         params, id )

    def info(self):
        return "Model version: " + self._version

    def _getService(self, mode: Mode):
        q_loader = QueryLoader(self._queries_path)

        return ServiceChatGPT(self._key, self._version, q_loader.getQueries(), **(Mode.as_args(mode)))

Endpoint.register(EndpointAsOpenAI)
