import os
import shutil
import tempfile
import unittest

from ecommquery.db.db import BaseModel
from ecommquery.db.map.Comment import Comment
from ecommquery.db.map.definitions.Partition import PartDef
from ecommquery.db.map.definitions.Property import PropDef
from ecommquery.db.map.definitions.Space import SpcDef


class TestTask(unittest.TestCase):

    def test_db_creation(self):
        tmpdir = tempfile.mkdtemp()
        dbfile_path = os.path.join(tmpdir, "miso.db")

        BaseModel.open(dbfile_path)
        #self.assertIsNotNone(db)


        shutil.rmtree(tmpdir)

    def test_db_mappings(self):
        tmpdir = tempfile.mkdtemp()
        dbfile_path = os.path.join(tmpdir, "miso.db")

        BaseModel.open(dbfile_path)
        #self.assertIsNotNone(db)

        comments = Comment.select().execute()
        self.assertEqual(comments[0].msg, 'Database has been created')

        spc1 = SpcDef.create(name='MySpace')

        self.assertEqual(spc1.name, 'MySpace')
        print('Assigned ID: ' + str(spc1.id))
        part1 = PartDef.create(spc = spc1, name = 'Part 1')

        self.assertEqual(part1.name, 'Part 1')

        # Real example
        stock = PropDef.create(ref_name = 'Stock', type = 'i', validator_fun = "test.fun", flags='P')
        price_ps = PropDef.create(ref_name='Price.6', type='i', validator_fun="test.fun", flags='P')
        price_alle = PropDef.create(ref_name='Price.2', type='i', validator_fun="test.fun", flags='P')
        ean_code = PropDef.create(ref_name='EAN', type='t', validator_fun="test.fun", flags='R')
        offerid = PropDef.create(ref_name='OfferID', type='i', validator_fun="test.fun", flags='R')

        shutil.rmtree(tmpdir)


