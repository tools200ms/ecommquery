from ecommquery import Endpoint
from ecommquery.assistant.openai.core.service_chatgpt import ServiceChatGPT
from ecommquery.core.validators import RegExValidator


class EndpointAsOpenAI(Endpoint):

    __models = ["gpt - 3.5 - turbo"]
    @staticmethod
    def reg_name():
        return 'chatgpt'

    @staticmethod
    def name():
        return "OpenAI ChatGPT API"

    @staticmethod
    def model_version_validator(name):
        return name.strip().lower() in EndpointAsOpenAI.__models

    def __init__(self, params: {}):
        super().__init__( {'version': Endpoint.Constr('_version',
                                    EndpointAsOpenAI.model_version_validator,
                                    EndpointAsOpenAI.__models[0] ),
                           'key': Endpoint.Constr(
                                        '_key',
                                        # don't do to strict validation, if API provider would
                                        # decide to support longer keys, or extend it by a low casec haracter cases
                                        # characters (assuming that UPPER case characters are curently used)
                                        # this code sould handle change without updates.
                                        # Exact validation is made by library that talks to API
                                        RegExValidator('[a-zA-Z0-9|\-|\_]{16,96}').validator)
                                    },
                         params )

    def info(self):
        if self._memo != None: return self._memo

        return ""

    def _getService(self):
        return ServiceChatGPT(self._key)

Endpoint.register(EndpointAsOpenAI)
