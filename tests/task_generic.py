import unittest
import sys

from ecommquery import Integrations
from ecommquery.core.loader_ini import IniLoader

sys.path.append('../ecommquery')

class TestTask(unittest.TestCase):
    def test_load_chatgpt(self):
        inegr = Integrations()
        inegr.addLoaderAndRead(IniLoader('./configurations/ai-chat_gpt.ini.test'))

        inegr.print()
        gpt = inegr.getService(endpoint="chatgpt")

        gpt.query('summary')

        self.assertEqual('0', '0')
