import os
import shutil
import tempfile
import unittest

from ecommquery.db.db import BaseModel
from ecommquery.db.map.Checkout import ObjCheckout
from ecommquery.db.map.Comment import Comment
from ecommquery.db.map.Object import Obj
from ecommquery.db.map.Property import ObjPropNoChange, ObjPropText, ObjPropInt
from ecommquery.db.map.definitions.Partition import PartDef
from ecommquery.db.map.definitions.Property import PropDef
from ecommquery.db.map.definitions.Sources import CheckoutSourceDef
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

        prop_int = PropDef.create(ref_name='INT', type='i', validator_fun="test.fun", flags='P')
        prop_txt = PropDef.create(ref_name='TEXT', type='t', validator_fun="test.fun", flags='P')
        ref_int = PropDef.create(ref_name='INT', type='i', validator_fun="test.fun", flags='R')
        ref_txt = PropDef.create(ref_name='TEXT', type='t', validator_fun="test.fun", flags='R')

        d_src1 = CheckoutSourceDef.create(name='DataSource1', part=part1)
        d_src2 = CheckoutSourceDef.create(name='DataSource2', part=part1)

        d_chained_src = CheckoutSourceDef.create(name='ChainedSource', part=part1, triggered_by=d_src1)

        chkout1_src1 = ObjCheckout.create(src=d_src1)
        chkout1_src2 = ObjCheckout.create(src=d_src2)

        # Add object properties
        ObjPropNoChange.create(obj=chkout1_src1, prop=prop_int)
        ObjPropText.create(obj=chkout1_src1, prop=prop_txt, value='Test')
        ObjPropInt.create(obj=chkout1_src1, prop=ref_int, value=123)

        shutil.rmtree(tmpdir)

    def test_db_realscenario(self):
        tmpdir = tempfile.mkdtemp()
        dbfile_path = os.path.join(tmpdir, "miso.db")

        BaseModel.open(dbfile_path)
        # self.assertIsNotNone(db)

        Comment.create(msg='Creating definitions for e-commerce scenario')

        products_spc = SpcDef.create(name='products')
        allegro_spc = SpcDef.create(name='allegro')
        presta_spc = SpcDef.create(name='prestashop')

        allegro_part = PartDef.create(spc=allegro_spc, name='clientid:0123456')
        presta_part = PartDef.create(spc=presta_spc, name='MyStore.com')

        # Real example
        stock = PropDef.create(ref_name = 'Stock', type = 'i', validator_fun = "stock", flags='P')
        ean_code = PropDef.create(ref_name='EAN', type='t', validator_fun="ean", flags='R')

        name = PropDef.create(ref_name='Name', spc=products_spc, type='t', validator_fun="name", flags='P')

        price_ps = PropDef.create(ref_name='Price', spc=presta_spc, type='i', validator_fun="price6", flags='P')
        price_alle = PropDef.create(ref_name='Price', spc=allegro_spc, type='i', validator_fun="price2", flags='P')

        offerid = PropDef.create(ref_name='OfferID', spc=allegro_spc, type='i', validator_fun="offer", flags='R')
        title = PropDef.create(ref_name='Title', type='t', validator_fun="name", flags='P')

        allegro_api = CheckoutSourceDef.create(name='Allegro API', part=allegro_part)
        presta_api = CheckoutSourceDef.create(name='Presta API', part=presta_part)

        obj = Obj.create()
        ObjCheckout.create(src=allegro_api)
        ObjCheckout.create(src=presta_api)

        #print('Temporary db: ' + dbfile_path)
        shutil.rmtree(tmpdir)

