
import json
from pprint import pprint

import openai
from openai import OpenAI

from ecommquery.core.service_analytical import AnalyticalService
from ecommquery.exceptions import CallError
from ecommquery.lib.product import Product


class ServiceChatGPT(AnalyticalService):
    def __init__(self, key: str, model_name: str, queries, verbose: bool = False):
        self.__verbose = verbose

        self.__client = OpenAI(api_key = key)
        self.__model_name = model_name

        self.__tomens_used = 0
        self.__queries = queries

    def product_prompt(self, text):
        return ""

    def query(self, name, params : []):
        q = self.__queries[name]

        return q.compileQueryText(params)

    def descr(self, text):
        try:
            response = self.__client.chat.completions.create(
                model= self.__model_name,
                messages=[
                    { "role": "assistant",
                      "content": self.product_prompt(text) },
                ],
                stream = False,
                max_tokens = 1080  # Maximum number of tokens to generate in the completion
            )

        except openai.RateLimitError as rl_err:
            raise CallError(rl_err)

        return self._process_answer(response)

    def test(self):
        try:
            # Request text completion
            response = self.__client.chat.completions.create(
                model= self.__model_name,
                messages=[
                    {"role": "assistant",
                     "content": "Say Hello in Polish. Provide JSON answer."},
                ],
                stream = False,
                max_tokens = 50  # Maximum number of tokens to generate in the completion
            )

        except openai.RateLimitError as rl_err:
            raise CallError(rl_err)

        return self._process_answer(response)

    def _process_answer(self, response):
        chooses_list = []
        j = None

        for ch in response.choices:
            j = json.loads(ch.message.content)
            chooses_list.append(j)

        return chooses_list

    def getTotalTokensUsed(self):
        return self.__tomens_used

    def close(self):
        if not self.__client.is_closed():
            self.__client.close()
