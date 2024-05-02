import unittest
import sys

from ecommquery import Integrations
from ecommquery.core.loader_ini import IniLoader
from ecommquery.lib.product import Product

sys.path.append('../ecommquery')

class TestTask(unittest.TestCase):

    def test_load_all_ds(self):
        inegr = Integrations()
        inegr.addLoaderAndRead(IniLoader('./configurations/ds-all.ini.test'))

        inegr.print()

    def test_load_chatgpt(self):
        inegr = Integrations()
        inegr.addLoaderAndRead(IniLoader('./configurations/ai-chat_gpt.ini.test'))

        inegr.print()
        gpt = inegr.getService(endpoint="chatgpt")

        prod = Product()

        prod.descr = "This is description"

        text = gpt.getPromptText('summary', [prod])
        print(text)

        self.assertEqual('0', '0')
