import unittest
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import src.clup.database.models as models
from src.clup.entities.store import Store
from src.clup.providers.sqlite.sqlite_store_provider \
    import SqliteStoreProvider


class TestSqliteStoreProvider(unittest.TestCase):
    def setUp(self):
        db_path = Path(__file__).parent
        self.db_file = db_path / Path('storeprovider_testdb.sqlite')
        self.engine = create_engine(f'sqlite:///{self.db_file}')
        models.Base.metadata.drop_all(self.engine)
        models.Base.metadata.create_all(self.engine)
        self.sp = SqliteStoreProvider(self.engine)

    def tearDown(self):
        self.db_file.unlink()

    def test_empty_sequence_returned_from_empty_db(self):
        stores = self.sp.get_stores()

        self.assertEqual(len(stores), 0)

    def test_all_stores_returned_from_non_empty_db(self):
        ms1 = models.Store(uuid='10', name='s1', address='via1', secret='key1')
        ms2 = models.Store(uuid='20', name='s2', address='via2', secret='key2')
        with Session(self.engine) as session, session.begin():
            session.add(ms1)
            session.add(ms2)

        stores = self.sp.get_stores()
        s1 = Store('10', 's1', 'via1', 'key1')
        s2 = Store('20', 's2', 'via2', 'key2')

        self.assertEqual(len(stores), 2)
        self.assertTrue(s1 in stores)
        self.assertTrue(s2 in stores)

    def test_store_is_added_to_db(self):
        s = Store('10', 's1', 'via1', 'key1')

        self.sp.add_store(s)

        with self.assertRaises(ValueError):
            self.sp.add_store(s)

        with Session(self.engine) as session, session.begin():
            stores = session.query(models.Store).all()
            store = stores[0]

            self.assertEqual(len(stores), 1)
            self.assertEqual(store.uuid, '10')
            self.assertEqual(store.name, 's1')
            self.assertEqual(store.address, 'via1')
            self.assertEqual(store.secret, 'key1')

    def test_store_is_retrieved_by_id(self):
        ms1 = models.Store(uuid='10', name='s1', address='via1', secret='key1')
        with Session(self.engine) as session, session.begin():
            session.add(ms1)

        store = self.sp.get_store('10')

        self.assertEqual(store.id, '10')
        self.assertEqual(store.name, 's1')
        self.assertEqual(store.address, 'via1')
        self.assertEqual(store.secret, 'key1')

    def test_store_is_updated(self):
        ms1 = models.Store(uuid='10', name='s1', address='via1', secret='key1')
        with Session(self.engine) as session, session.begin():
            session.add(ms1)
        updated_store = Store('10', 'news1', 'newvia1', 'newkey1')

        self.sp.update_store(updated_store)

        with Session(self.engine) as session, session.begin():
            stores = session.query(models.Store).all()
            store = stores[0]

            self.assertEqual(len(stores), 1)
            self.assertEqual(store.uuid, '10')
            self.assertEqual(store.name, 'news1')
            self.assertEqual(store.address, 'newvia1')
            self.assertEqual(store.secret, 'newkey1')

    def test_store_and_relative_aisles_are_removed_from_db(self):
        ms1 = models.Store(uuid='10', name='s1', address='via1', secret='key1')
        ma1 = models.Aisle(uuid='100', name='a1', categories='1', capacity=5)
        ma2 = models.Aisle(uuid='200', name='a2', categories='2', capacity=7)
        msa1 = models.StoreAisle(store_uuid='10', aisle_uuid='100')
        msa2 = models.StoreAisle(store_uuid='10', aisle_uuid='200')
        with Session(self.engine) as session, session.begin():
            session.add(ms1)
            session.add(ma1)
            session.add(ma2)
            session.add(msa1)
            session.add(msa2)

        self.sp.delete_store('10')
        with self.assertRaises(ValueError):
            self.sp.delete_store('10')

        with Session(self.engine) as session, session.begin():
            stores = session.query(models.Store).all()
            aisles = session.query(models.Aisle).all()
            store_aisles = session.query(models.StoreAisle).all()

            self.assertEqual(len(stores), 0)
            self.assertEqual(len(aisles), 0)
            self.assertEqual(len(store_aisles), 0)

    def test_store_admin_ids_retrieved(self):
        ms1 = models.Store(uuid='10', name='s1', address='via1', secret='key1')
        msa1 = models.StoreAdmin(store_uuid='10', admin_uuid='100')
        msa2 = models.StoreAdmin(store_uuid='10', admin_uuid='200')
        with Session(self.engine) as session, session.begin():
            session.add(ms1)
            session.add(msa1)
            session.add(msa2)

        admin_ids = self.sp.get_admin_ids('10')

        self.assertEqual(len(admin_ids), 2)
        self.assertTrue('100' in admin_ids)
        self.assertTrue('200' in admin_ids)

    def test_store_id_from_name_return_correct_value(self):
        ms1 = models.Store(uuid='10', name='s1', address='via1', secret='key1')
        ms2 = models.Store(uuid='20', name='s2', address='via2', secret='key2')
        with Session(self.engine) as session, session.begin():
            session.add(ms1)
            session.add(ms2)
        sp = SqliteStoreProvider(self.engine)

        store1_id = sp.get_store_id_from_name_and_address('s1', 'via1')
        store2_id = sp.get_store_id_from_name_and_address('s2', 'via2')

        self.assertEqual(store1_id, '10')
        self.assertEqual(store2_id, '20')

        with self.assertRaises(ValueError):
            sp.get_store_id_from_name_and_address('s1', 'via2')
