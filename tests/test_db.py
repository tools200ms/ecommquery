import os
import shutil
import tempfile
import unittest
from datetime import datetime
from pprint import pprint

from ecommquery.db.db import Db
from ecommquery.db.map.Comment import Comment


class TestTask(unittest.TestCase):

    def test_db_creation(self):
        tmpdir = tempfile.mkdtemp()
        dbfile_path = os.path.join(tmpdir, "miso.db")

        Db.open(dbfile_path)
        #self.assertIsNotNone(db)
        
        # db.close()

        shutil.rmtree(tmpdir)

    def test_db_mappings(self):
        tmpdir = tempfile.mkdtemp()
        dbfile_path = os.path.join(tmpdir, "miso.db")

        Db.open(dbfile_path)
        #self.assertIsNotNone(db)

        query = Comment.select()
        pprint(query.sql())
        for row in query:
            print(row.msg)
        # db.close()

        shutil.rmtree(tmpdir)


