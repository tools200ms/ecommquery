
import json
from pprint import pprint

import openai
from openai import OpenAI

from ecommquery.core.service_analytical import AnalyticalService
from ecommquery.exceptions import CallError


class ServiceChatGPT(AnalyticalService):
    def __init__(self, key: str, model_name: str, verbose: bool = False):
        self.__verbose = verbose

        self.__client = OpenAI(api_key = key)
        self.__model_name = model_name

        self.__tomens_used = 0

    def product_prompt(self, text):
        return "Can you determine categories and attributes that fits to the following product description that is in a Polish language?: \n\n" + \
                text + \
                "\n\nAim to find multiple categories, avoid details regarding product ingredients, nutritions and origin. \n" + \
                "Try to assign generic names for categories. \n" + \
                "Return also product speciffic attributes. \n" + \
                "Categories and sub-categories should be outputed as an array of strings sorted by relevance (most relevant as first), this array should be under 'kategorie' key. \n" + \
                "Number of categories should be between one and three. \n" + \
                "JSON keys should start by capital letter, followed by lowercase characters, values can't be objects, only arrays and strings are allowed. \n" + \
                "Format output in JSON, provide results in Polish language."

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
