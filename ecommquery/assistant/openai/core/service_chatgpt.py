from pprint import pprint

import openai
from openai import OpenAI

from ecommquery.core.service_analytical import AnalyticalService
from ecommquery.exceptions import CallError


class ServiceChatGPT(AnalyticalService):
    def __init__(self, key, verbose = False):
        self.__verbose = verbose

        client = OpenAI(api_key = key)

        try:
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                {"role": "user",
                 "content": "Say Hello in Polish"},
                ]
            )

            pprint(completion)
        except openai.RateLimitError as rl_err:
            raise CallError(rl_err)

        #stream = client.chat.completions.create(
        #    model="gpt-4",
        #    messages=[{"role": "user", "content": "Say this is a test"}],
        #    stream=True,
        #)
        #for chunk in stream:
        #    if chunk.choices[0].delta.content is not None:
        #        print(chunk.choices[0].delta.content, end="")

