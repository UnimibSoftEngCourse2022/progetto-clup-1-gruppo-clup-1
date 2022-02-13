import unittest
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.clup.entities.admin import Admin
import src.clup.database.models as models
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
        ma1 = models.Admin(uuid='10', username='u1', password='p1')
        ma2 = models.Admin(uuid='20', username='u2', password='p2')
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
            admins = session.query(models.Admin).all()
            admin = admins[0]

            self.assertEqual(len(admins), 1)
            self.assertEqual(admin.uuid, '10')
            self.assertEqual(admin.username, 'u1')
            self.assertEqual(admin.password, 'p1')

    def test_admin_is_removed_from_db(self):
        ma1 = models.Admin(uuid='10', username='u1', password='p1')
        with Session(self.engine) as session, session.begin():
            session.add(ma1)

        self.ap.remove_admin('10')

        with Session(self.engine) as session, session.begin():
            admins = session.query(models.Admin).all()

            self.assertEqual(len(admins), 0)

    def test_admin_is_updated(self):
        ma1 = models.Admin(uuid='10', username='u1', password='p1')
        with Session(self.engine) as session, session.begin():
            session.add(ma1)
        updated_admin = Admin('10', 'newu1', 'newp1')

        self.ap.update_admin(updated_admin)

        with Session(self.engine) as session, session.begin():
            admins = session.query(models.Admin).all()
            admin = admins[0]

            self.assertEqual(len(admins), 1)
            self.assertEqual(admin.uuid, '10')
            self.assertEqual(admin.username, 'newu1')
            self.assertEqual(admin.password, 'newp1')

    def test_admin_store_id_is_returned(self):
        msa = models.StoreAdmin(admin_uuid='10', store_uuid='100')
        with Session(self.engine) as session, session.begin():
            session.add(msa)

        store_id = self.ap.get_store_id('10')

        self.assertEqual(store_id, '100')
