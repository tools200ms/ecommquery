from openai import OpenAI

from ecommquery import Endpoint


class EndpointAsOpenAI(Endpoint):

    @staticmethod
    def reg_name():
        return 'presta_api'



client = OpenAI()

stream = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Say this is a test"}],
    stream=True,
)
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
