import os
import shutil
import tempfile
import unittest
from datetime import datetime

from ecommquery.db.db import Db

class TestTask(unittest.TestCase):

    def test_db_creation(self):
        tmpdir = tempfile.mkdtemp()
        dbfile_path = os.path.join(tmpdir, "miso.db")

        db = Db.open(dbfile_path)
        self.assertIsNotNone(db)
        db.close()

        shutil.rmtree(tmpdir)

