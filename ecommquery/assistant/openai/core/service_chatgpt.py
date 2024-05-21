
import json
from pprint import pprint

import openai
from openai import OpenAI

from ecommquery.core.service_analytical import AnalyticalService
from ecommquery.exceptions import CallError
from ecommquery.lib.product import Product


class ServiceChatGPT(AnalyticalService):
    def __init__(self, key: str, model_name: str, queries, verbose: bool, debug: bool, pretend: bool):
        self.__verbose = verbose
        self.__debug = debug

        if pretend:
            # echo mode
            self.sendPrompt = self.echoPromptMsg
        else:
            self.sendPrompt = self.sendPromptMsg

        self.__client = OpenAI(api_key = key)
        self.__model_name = model_name

        self.__tomens_used = 0
        self.__queries = queries

    def echoPromptMsg(self, name, params : []):
        q = self.__queries[name]

        return q.compileQueryText(params)

    def sendPromptMsg(self, name, params : []):
        q = self.__queries[name]

        prompt = q.compileQueryText(params)

        try:
            response = self.__client.chat.completions.create(
                model = self.__model_name,
                messages = [
                    { "role": "assistant",
                      "content": prompt },
                ],
                functions = [
                { "name": "createResultObject",
                  "parameters": {
                        "type": "object",
                        "properties": {
                            "first_sentence_of_point_3": {
                                "type": "string"
                            },
                            "error": {
                                "type": "string"
                            }
                        }
                    }
                }],
                function_call = {"name": "createResultObject"},
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
            try:
                functionCall = ch.message.function_call
                print("BEGIN: \n" + functionCall.arguments + "\nEND--")
                j = json.loads(functionCall.arguments)

                chooses_list.append(j)
            except json.decoder.JSONDecodeError:
                print("JSON decoder exception")
                pprint(ch.message.content)

        return chooses_list

    def getTotalTokensUsed(self):
        return self.__tomens_used

    def close(self):
        if not self.__client.is_closed():
            self.__client.close()
