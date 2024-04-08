
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

    def descr(self, text):
        msg = "Can you determine categories and attributes that fits to the following product description that is in a Polish language?: \n\n" + \
                text + "\n\nAim to generate multiple categories, avoid details regarding product ingredients. Return an answer in JSON format with results in Polish language"

        try:
            response = self.__client.chat.completions.create(
                model= self.__model_name,
                messages=[
                    { "role": "assistant",
                      "content": msg },
                ],
                max_tokens = 150  # Maximum number of tokens to generate in the completion
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
                max_tokens = 50  # Maximum number of tokens to generate in the completion
            )

        except openai.RateLimitError as rl_err:
            raise CallError(rl_err)

        return self._process_answer(response)

    def _process_answer(self, response):
        chooses_list = []
        for ch in response.choices:
            #self.__tomens_used += ch.total_tokens
            pprint(ch)
            # chooses_list.append(json.loads(ch.message.content))
            chooses_list.append(ch.message.content)

        return chooses_list

    def getTotalTokensUsed(self):
        return self.__tomens_used

        #stream = client.chat.completions.create(
        #    model="gpt-4",
        #    messages=[{"role": "user", "content": "Say this is a test"}],
        #    stream=True,
        #)
        #for chunk in stream:
        #    if chunk.choices[0].delta.content is not None:
        #        print(chunk.choices[0].delta.content, end="")

    def close(self):
        if not self.__client.is_closed():
            self.__client.close()
