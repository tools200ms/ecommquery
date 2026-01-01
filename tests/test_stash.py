import os
import shutil
from datetime import datetime
import json
import unittest
import sys
import tempfile
from pathlib import Path

from ecommquery.core.stash import Stash


sys.path.append('../ecommquery')

class TestTask(unittest.TestCase):

    def test_1(self):
        tmpdir = tempfile.mkdtemp()
        temp_file = os.path.join(tmpdir, "stash.sql")

        print(f"Temporary file '{temp_file}' has been created.")

        stash_1g = Stash('test', 'id', Path(temp_file))
        stash_1g.load()

        stash_1g.set('prop_a', 1)
        stash_1g.set('prop_b', "test")

        stash_1g.save()

        with open(temp_file) as temp_file_ref2:
            copy = json.load(temp_file_ref2)

        self.assertEqual( copy['test']['id']['prop_a'], 1 )
        self.assertEqual( copy['test']['id']['prop_b'], "test")

        with self.assertRaises(Exception):
            Stash('test', 'id', Path(temp_file))

        stash_1g.close()
        stash_2g = Stash('test', 'id', Path(temp_file))

        stash_2g.load()

        self.assertEqual( stash_2g.get('prop_a'), 1 )
        self.assertEqual( stash_2g.get('prop_b'), "test")

        self.assertEqual(stash_2g.get('not_existing'), None)

        stash_2g.set('prop_a', 2)
        stash_2g.unset('prop_b')

        stash_2g.save()

        with open(temp_file) as temp_file_ref2:
            copy = json.load(temp_file_ref2)

        self.assertEqual( copy['test']['id']['prop_a'], 2 )
        self.assertNotIn('prop_b', copy['test']['id'])

        date_now = datetime.now()
        date_now_str = date_now.strftime('%Y-%m-%d %H:%M:%S')
        date_now_norm = datetime.strptime(date_now_str, '%Y-%m-%d %H:%M:%S')

        stash_2g.setDate('date_now', date_now)

        self.assertEqual( date_now_str,
                          stash_2g.get('date_now') )

        self.assertEqual(date_now_norm,
                         stash_2g.getDate('date_now') )

        stash_2g.set('none_value', None)
        self.assertEqual(None,
                         stash_2g.get('none_value'))

        stash_2g.save()
        stash_2g.close()

        shutil.rmtree(tmpdir)
