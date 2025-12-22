import unittest
import sys
import tempfile
from pathlib import Path

from ecommquery.core.stash import Stash


sys.path.append('../ecommquery')

class TestTask(unittest.TestCase):

    def test_1(self):
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        temp_file.close()
        print(f"Temporary file '{temp_file.name}' has been created.")

        stash_1g = Stash('test', 'id', Path(temp_file.name))
        stash_1g.load()

        stash_1g.set('prop_a', 1)
        stash_1g.set('prop_b', "test")

        stash_1g.save()

        #stash_2g = Stash('test', 'id', Path(temp_file.name))
        #stash_2g.load()

        #self.assertEqual( stash_2g.get('prop_a'), 1 )
        #self.assertEqual( stash_2g.get('prop_b'), "test")


   