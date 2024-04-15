from ecommquery import Endpoint
from ecommquery.assistant.lib.query_loader import QueryLoader
from ecommquery.assistant.openai.core.service_chatgpt import ServiceChatGPT
from ecommquery.core.validators import RegExValidator, ListValidator, PathValidator


class EndpointAsOpenAI(Endpoint):

    @staticmethod
    def reg_name():
        return 'chatgpt'

    @staticmethod
    def name():
        return "OpenAI ChatGPT API"

    def __init__(self, params: {}):
        super().__init__( {'version': Endpoint.Constr('_version',
                                    ListValidator(["gpt-3.5-turbo"], 0) ),
                           'key': Endpoint.Constr(
                                        '_key',
                                        # don't do to strict validation, if API provider would
                                        # decide to support longer keys, or extend it by a low casec haracter cases
                                        # characters (assuming that UPPER case characters are curently used)
                                        # this code sould handle change without updates.
                                        # Exact validation is made by library that talks to API
                                        RegExValidator('[a-zA-Z0-9|\-|\_]{16,96}')),
                           'queries': Endpoint.Constr('_queries_path', PathValidator('queries'))
                                    },
                         params )

    def info(self):
        return "Model version: " + self._version

    def _getService(self):
        q_loader = QueryLoader(self._queries_path)

        return ServiceChatGPT(self._key, self._version, q_loader.getQueries())

Endpoint.register(EndpointAsOpenAI)
