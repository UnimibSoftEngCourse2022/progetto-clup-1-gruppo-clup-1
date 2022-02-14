import unittest
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import src.clup.database.models as models
from src.clup.entities.aisle import Aisle
from src.clup.entities.category import Category
from src.clup.providers.sqlite_aisle_provider import SqliteAisleProvider


class TestSqliteAisleProvider(unittest.TestCase):
    def setUp(self):
        db_path = Path(__file__).parent
        self.db_file = db_path / Path('aisleprovider_testdb.sqlite')
        self.engine = create_engine(f'sqlite:///{self.db_file}')
        models.Base.metadata.drop_all(self.engine)
        models.Base.metadata.create_all(self.engine)
        self.ap = SqliteAisleProvider(self.engine)

    def tearDown(self):
        self.db_file.unlink()

    def test_empty_sequence_returned_from_empty_db(self):
        aisles = self.ap.get_aisles()

        self.assertEqual(len(aisles), 0)

    def test_all_aisles_returned_from_non_empty_db(self):
        ma1 = models.Aisle(uuid='10', name='a1', categories='1,2', capacity=10)
        ma2 = models.Aisle(uuid='20', name='a2', categories='3,4', capacity=5)
        with Session(self.engine) as session, session.begin():
            session.add(ma1)
            session.add(ma2)

        aisles = self.ap.get_aisles()
        a1 = Aisle('10', 'a1', (Category(1), Category(2)), 10)
        a2 = Aisle('20', 'a2', (Category(3), Category(4)), 5)

        self.assertEqual(len(aisles), 2)
        self.assertTrue(a1 in aisles)
        self.assertTrue(a2 in aisles)

    def test_all_and_only_store_aisles_returned(self):
        ma1 = models.Aisle(uuid='10', name='a1', categories='1,2', capacity=10)
        ma2 = models.Aisle(uuid='20', name='a2', categories='3,4', capacity=5)
        ma3 = models.Aisle(uuid='30', name='a3', categories='2,4', capacity=7)
        msa1 = models.StoreAisle(store_uuid='100', aisle_uuid='10')
        msa2 = models.StoreAisle(store_uuid='200', aisle_uuid='20')
        msa3 = models.StoreAisle(store_uuid='200', aisle_uuid='30')
        with Session(self.engine) as session, session.begin():
            session.add(ma1)
            session.add(ma2)
            session.add(ma3)
            session.add(msa1)
            session.add(msa2)
            session.add(msa3)

        aisles = self.ap.get_store_aisles('200')
        a2 = Aisle('20', 'a2', (Category(3), Category(4)), 5)
        a3 = Aisle('30', 'a3', (Category(2), Category(4)), 7)

        self.assertEqual(len(aisles), 2)
        self.assertTrue(a2 in aisles)
        self.assertTrue(a3 in aisles)

    def test_all_and_only_store_aisle_ids_returned(self):
        ma1 = models.Aisle(uuid='10', name='a1', categories='1,2', capacity=10)
        ma2 = models.Aisle(uuid='20', name='a2', categories='3,4', capacity=5)
        ma3 = models.Aisle(uuid='30', name='a3', categories='2,4', capacity=7)
        msa1 = models.StoreAisle(store_uuid='100', aisle_uuid='10')
        msa2 = models.StoreAisle(store_uuid='200', aisle_uuid='20')
        msa3 = models.StoreAisle(store_uuid='200', aisle_uuid='30')
        with Session(self.engine) as session, session.begin():
            session.add(ma1)
            session.add(ma2)
            session.add(ma3)
            session.add(msa1)
            session.add(msa2)
            session.add(msa3)

        aisle_ids = self.ap.get_store_aisle_ids('200')

        self.assertEqual(len(aisle_ids), 2)
        self.assertTrue('20' in aisle_ids)
        self.assertTrue('30' in aisle_ids)

    def test_aisle_is_added_to_db(self):
        a = Aisle('10', 'a1', (Category(1), Category(2)), 5)

        self.ap.add_aisle('100', a)

        with Session(self.engine) as session, session.begin():
            aisles = session.query(models.Aisle).all()
            aisle = aisles[0]
            store_aisles = session.query(models.StoreAisle).all()
            store_aisle = store_aisles[0]

            self.assertEqual(len(aisles), 1)
            self.assertEqual(aisle.uuid, '10')
            self.assertEqual(aisle.name, 'a1')
            self.assertEqual(aisle.categories, '1,2')
            self.assertEqual(aisle.capacity, 5)
            self.assertEqual(len(store_aisles), 1)
            self.assertEqual(store_aisle.store_uuid, '100')
            self.assertEqual(store_aisle.aisle_uuid, '10')

    def test_aisle_is_added_to_db_with_categories_stored(self):
        a = Aisle('10', 'a1', (Category(4), Category(2)), 5)

        self.ap.add_aisle('100', a)

        with Session(self.engine) as session, session.begin():
            aisles = session.query(models.Aisle).all()
            aisle = aisles[0]

            self.assertEqual(len(aisles), 1)
            self.assertEqual(aisle.uuid, '10')
            self.assertEqual(aisle.name, 'a1')
            self.assertEqual(aisle.categories, '2,4')
            self.assertEqual(aisle.capacity, 5)

    def test_aisle_is_removed(self):
        ma = models.Aisle(uuid='10', name='a1', categories='1,2', capacity=10)
        msa = models.StoreAisle(store_uuid='100', aisle_uuid='10')
        with Session(self.engine) as session, session.begin():
            session.add(ma)
            session.add(msa)

        self.ap.remove_aisle('10')

        with Session(self.engine) as session, session.begin():
            aisles = session.query(models.Aisle).all()
            store_aisles = session.query(models.StoreAisle).all()

            self.assertEqual(len(aisles), 0)
            self.assertEqual(len(store_aisles), 0)

    def test_aisle_is_updated(self):
        ma = models.Aisle(uuid='10', name='a1', categories='1,2', capacity=10)
        with Session(self.engine) as session, session.begin():
            session.add(ma)
        a = Aisle('10', 'newa1', (Category(3), Category(4)), 5)

        self.ap.update_aisle(a)

        with Session(self.engine) as session, session.begin():
            aisles = session.query(models.Aisle).all()
            aisle = aisles[0]

            self.assertEqual(len(aisles), 1)
            self.assertEqual(aisle.uuid, '10')
            self.assertEqual(aisle.name, 'newa1')
            self.assertEqual(aisle.categories, '3,4')
            self.assertEqual(aisle.capacity, 5)
