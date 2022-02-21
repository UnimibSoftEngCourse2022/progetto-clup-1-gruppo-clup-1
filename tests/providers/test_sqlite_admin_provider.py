import unittest
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import src.clup.database.models as models
from src.clup.entities.admin import Admin
from src.clup.providers.sqlite_admin_provider \
    import SqliteAdminProvider


class TestSqliteAdminProvider(unittest.TestCase):
    def setUp(self):
        db_path = Path(__file__).parent
        self.db_file = db_path / Path('adminprovider_testdb.sqlite')
        self.engine = create_engine(f'sqlite:///{self.db_file}')
        models.Base.metadata.drop_all(self.engine)
        models.Base.metadata.create_all(self.engine)
        self.ap = SqliteAdminProvider(self.engine)

    def tearDown(self):
        self.db_file.unlink()

    def test_empty_sequence_returned_from_empty_db(self):
        admins = self.ap.get_admins()

        self.assertEqual(len(admins), 0)

    def test_all_admins_returned_from_non_empty_db(self):
        ma1 = models.Account(uuid='10', username='u1', password='p1', type='admin')
        ma2 = models.Account(uuid='20', username='u2', password='p2', type='admin')
        with Session(self.engine) as session, session.begin():
            session.add(ma1)
            session.add(ma2)

        admins = self.ap.get_admins()
        a1 = Admin('10', 'u1', 'p1')
        a2 = Admin('20', 'u2', 'p2')

        self.assertEqual(len(admins), 2)
        self.assertTrue(a1 in admins)
        self.assertTrue(a2 in admins)

    def test_admin_is_added_to_db(self):
        a = Admin('10', 'u1', 'p1')

        self.ap.add_admin(a)

        with Session(self.engine) as session, session.begin():
            admins = session.query(models.Account).filter(models.Account.type == 'admin').all()
            admin = admins[0]

            self.assertEqual(len(admins), 1)
            self.assertEqual(admin.uuid, '10')
            self.assertEqual(admin.username, 'u1')
            self.assertEqual(admin.password, 'p1')

    def test_admin_is_removed_from_db(self):
        ma1 = models.Account(uuid='10', username='u1', password='p1', type='admin')
        with Session(self.engine) as session, session.begin():
            session.add(ma1)

        self.ap.remove_admin('10')

        with Session(self.engine) as session, session.begin():
            admins = session.query(models.Account).filter(models.Account.type == 'admin').all()

            self.assertEqual(len(admins), 0)

    def test_admin_is_updated(self):
        ma1 = models.Account(uuid='10', username='u1', password='p1', type='admin')
        with Session(self.engine) as session, session.begin():
            session.add(ma1)
        updated_admin = Admin('10', 'newu1', 'newp1')

        self.ap.update_admin(updated_admin)

        with Session(self.engine) as session, session.begin():
            admins = session.query(models.Account). filter(models.Account.type == 'admin').all()
            admin = admins[0]

            self.assertEqual(len(admins), 1)
            self.assertEqual(admin.uuid, '10')
            self.assertEqual(admin.username, 'newu1')
            self.assertEqual(admin.password, 'newp1')

    def test_admin_store_id_is_returned(self):
        ma1 = models.Account(uuid='10', username='u1', password='p1', type='admin')
        msa = models.StoreAdmin(admin_uuid='10', store_uuid='100')
        with Session(self.engine) as session, session.begin():
            session.add(ma1)
            session.add(msa)

        store_id = self.ap.get_store_id('10')

        self.assertEqual(store_id, '100')

    def test_admin_store_pair_is_added_to_table(self):
        self.ap.add_admin_to_store('10', '200')

        with Session(self.engine) as session, session.begin():
            store_admins = session.query(models.StoreAdmin).all()
            store_admin = store_admins[0]

            self.assertEqual(len(store_admins), 1)
            self.assertEqual(store_admin.admin_uuid, '10')
            self.assertEqual(store_admin.store_uuid, '200')


class TestSqliteAdminProviderIdValidation(unittest.TestCase):
    def setUp(self):
        db_path = Path(__file__).parent
        self.db_file = db_path / Path('adminprovider2_testdb.sqlite')
        self.engine = create_engine(f'sqlite:///{self.db_file}')
        models.Base.metadata.drop_all(self.engine)
        models.Base.metadata.create_all(self.engine)
        self.ap = SqliteAdminProvider(self.engine)

    def tearDown(self):
        self.db_file.unlink()

    def test_duplicate_id_throws(self):
        ma1 = models.Account(uuid='10', username='u1', password='p1', type='admin')
        with Session(self.engine) as session, session.begin():
            session.add(ma1)
        a = Admin('10', 'admin', 'pwd')

        with self.assertRaises(ValueError):
            self.ap.add_admin(a)

    def test_duplicate_username_throws(self):
        ma1 = models.Account(uuid='10', username='u1', password='p1', type='admin')
        with Session(self.engine) as session, session.begin():
            session.add(ma1)
        a = Admin('100', 'u1', 'pwd')

        with self.assertRaises(ValueError):
            self.ap.add_admin(a)

    def test_remove_on_unexistent_id_throws(self):
        ma1 = models.Account(uuid='10', username='u1', password='p1', type='admin')
        with Session(self.engine) as session, session.begin():
            session.add(ma1)

        with self.assertRaises(ValueError):
            self.ap.remove_admin('100')

    def test_update_on_unexistent_id_throws(self):
        ma1 = models.Account(uuid='10', username='u1', password='p1', type='admin')
        with Session(self.engine) as session, session.begin():
            session.add(ma1)
        a = Admin('100', 'u1', 'pwd')

        with self.assertRaises(ValueError):
            self.ap.update_admin(a)

    def test_get_store_id_on_unexistent_id_throws(self):
        with self.assertRaises(ValueError):
            self.ap.get_store_id('10')

    def test_giving_more_than_one_store_to_admin_throws(self):
        msa = models.StoreAdmin(admin_uuid='10', store_uuid='200')
        with Session(self.engine) as session, session.begin():
            session.add(msa)

        with self.assertRaises(ValueError):
            self.ap.add_admin_to_store('10', '300')
