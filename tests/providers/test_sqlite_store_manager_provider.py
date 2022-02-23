import unittest
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import src.clup.database.models as models
from src.clup.entities.store_manager import StoreManager
from src.clup.providers.sqlite_store_manager_provider \
    import SqliteStoreManagerProvider


class TestSqliteStoreManagerProvider(unittest.TestCase):
    def setUp(self):
        db_path = Path(__file__).parent
        self.db_file = db_path / Path('store_managerprovider_testdb.sqlite')
        self.engine = create_engine(f'sqlite:///{self.db_file}')
        models.Base.metadata.drop_all(self.engine)
        models.Base.metadata.create_all(self.engine)
        self.smp = SqliteStoreManagerProvider(self.engine)

    def tearDown(self):
        self.db_file.unlink()

    def test_empty_sequence_returned_from_empty_db(self):
        store_managers = self.smp.get_store_managers()

        self.assertEqual(len(store_managers), 0)

    def test_all_store_managers_returned_from_non_empty_db(self):
        ma1 = models.Account(uuid='10', username='u1', password_hash='p1', type='store_manager')
        ma2 = models.Account(uuid='20', username='u2', password_hash='p2', type='store_manager')
        with Session(self.engine) as session, session.begin():
            session.add(ma1)
            session.add(ma2)

        store_managers = self.smp.get_store_managers()
        a1 = StoreManager('10', 'u1', 'p1')
        a2 = StoreManager('20', 'u2', 'p2')

        self.assertEqual(len(store_managers), 2)
        self.assertTrue(a1 in store_managers)
        self.assertTrue(a2 in store_managers)

    def test_store_manager_is_added_to_db(self):
        a = StoreManager('10', 'u1', 'p1')

        self.smp.add_manager(a)

        with Session(self.engine) as session, session.begin():
            store_managers = session.query(models.Account).filter(models.Account.type == 'store_manager').all()
            store_manager = store_managers[0]

            self.assertEqual(len(store_managers), 1)
            self.assertEqual(store_manager.uuid, '10')
            self.assertEqual(store_manager.username, 'u1')
            self.assertEqual(store_manager.password_hash, 'p1')

    def test_store_manager_is_removed_from_db(self):
        ma1 = models.Account(uuid='10', username='u1', password_hash='p1', type='store_manager')
        with Session(self.engine) as session, session.begin():
            session.add(ma1)

        self.smp.delete_store_manager('10')

        with Session(self.engine) as session, session.begin():
            store_managers = session.query(models.Account).filter(models.Account.type == 'store_manager').all()

            self.assertEqual(len(store_managers), 0)

    def test_store_manager_is_updated(self):
        ma1 = models.Account(uuid='10', username='u1', password_hash='p1', type='store_manager')
        with Session(self.engine) as session, session.begin():
            session.add(ma1)
        updated_store_manager = StoreManager('10', 'newu1', 'newp1')

        self.smp.update(updated_store_manager)

        with Session(self.engine) as session, session.begin():
            store_managers = session.query(models.Account).filter(models.Account.type == 'store_manager').all()
            store_manager = store_managers[0]

            self.assertEqual(len(store_managers), 1)
            self.assertEqual(store_manager.uuid, '10')
            self.assertEqual(store_manager.username, 'newu1')
            self.assertEqual(store_manager.password_hash, 'newp1')

    def test_store_manager_is_returned(self):
        ma1 = models.Account(uuid='10', username='u1', password_hash='p1', type='store_manager')
        with Session(self.engine) as session, session.begin():
            session.add(ma1)

        manager = self.smp.get_manager('10')
        expected_manager = StoreManager('10', 'u1', 'p1')

        self.assertEqual(manager, expected_manager)

    def test_id_is_returned_from_secret(self):
        ms_pair = models.StoreManagerSecretKey(store_manager_uuid='sm',
                                               secret_key='sk',
                                               active=False)
        with Session(self.engine) as session, session.begin():
            session.add(ms_pair)

        mgr_id = self.smp.get_id_from_secret('sk')

        self.assertEqual(mgr_id, 'sm')


class TestSqliteStoreManagerProviderIdValidation(unittest.TestCase):
    def setUp(self):
        db_path = Path(__file__).parent
        self.db_file = db_path / Path('store_managerprovider2_testdb.sqlite')
        self.engine = create_engine(f'sqlite:///{self.db_file}')
        models.Base.metadata.drop_all(self.engine)
        models.Base.metadata.create_all(self.engine)
        self.smp = SqliteStoreManagerProvider(self.engine)

    def tearDown(self):
        self.db_file.unlink()

    def test_duplicate_id_throws(self):
        ma1 = models.Account(uuid='10', username='u1', password_hash='p1', type='store_manager')
        with Session(self.engine) as session, session.begin():
            session.add(ma1)
        a = StoreManager('10', 'store_manager', 'pwd')

        with self.assertRaises(ValueError):
            self.smp.add_manager(a)

    def test_duplicate_username_throws(self):
        ma1 = models.Account(uuid='10', username='u1', password_hash='p1', type='store_manager')
        with Session(self.engine) as session, session.begin():
            session.add(ma1)
        a = StoreManager('100', 'u1', 'pwd')

        with self.assertRaises(ValueError):
            self.smp.add_manager(a)

    def test_remove_on_unexistent_id_throws(self):
        ma1 = models.Account(uuid='10', username='u1', password_hash='p1', type='store_manager')
        with Session(self.engine) as session, session.begin():
            session.add(ma1)

        with self.assertRaises(ValueError):
            self.smp.delete_store_manager('100')

    @unittest.skip('update not implemented yet')
    def test_update_on_unexistent_id_throws(self):
        ma1 = models.Account(uuid='10', username='u1', password_hash='p1', type='store_manager')
        with Session(self.engine) as session, session.begin():
            session.add(ma1)
        a = StoreManager('100', 'u1', 'pwd')

        with self.assertRaises(ValueError):
            self.smp.update_store_manager(a)

    def test_get_store_id_on_unexistent_id_throws(self):
        with self.assertRaises(ValueError):
            self.smp.get_manager('10')
