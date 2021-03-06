import unittest
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import src.clup.database.models as models
from src.clup.entities.user import User
from src.clup.providers.sqlite.sqlite_user_provider \
    import SqliteUserProvider


class TestSqliteUserProvider(unittest.TestCase):
    def setUp(self):
        db_path = Path(__file__).parent
        self.db_file = db_path / Path('userprovider_testdb.sqlite')
        self.engine = create_engine(f'sqlite:///{self.db_file}')
        models.Base.metadata.drop_all(self.engine)
        models.Base.metadata.create_all(self.engine)
        self.up = SqliteUserProvider(self.engine)

    def tearDown(self):
        self.db_file.unlink()

    def test_empty_sequence_returned_from_empty_db(self):
        users = self.up.get_users()

        self.assertEqual(len(users), 0)

    def test_all_users_returned_from_non_empty_db(self):
        mu1 = models.Account(uuid='10', username='u1', password_hash='p1', type='user')
        mu2 = models.Account(uuid='20', username='u2', password_hash='p2', type='user')
        with Session(self.engine) as session, session.begin():
            session.add(mu1)
            session.add(mu2)

        users = self.up.get_users()
        u1 = User('10', 'u1', 'p1')
        u2 = User('20', 'u2', 'p2')

        self.assertEqual(len(users), 2)
        self.assertTrue(u1 in users)
        self.assertTrue(u2 in users)

    def test_user_is_added_to_db(self):
        u = User('10', 'u1', 'p1')

        self.up.add_user(u)
        with self.assertRaises(ValueError):
            self.up.add_user(u)

        with Session(self.engine) as session, session.begin():
            users = session.query(models.Account).filter(models.Account.type == 'user').all()
            user = users[0]

            self.assertEqual(len(users), 1)
            self.assertEqual(user.uuid, '10')
            self.assertEqual(user.username, 'u1')
            self.assertEqual(user.password_hash, 'p1')

    def test_user_is_removed_from_db(self):
        mu1 = models.Account(uuid='10', username='u1', password_hash='p1', type='user')
        with Session(self.engine) as session, session.begin():
            session.add(mu1)

        with self.assertRaises(ValueError):
            self.up.remove_user('not_existing_id')
        self.up.remove_user('10')

        with Session(self.engine) as session, session.begin():
            users = session.query(models.Account).filter(models.Account.type == 'user').all()

            self.assertEqual(len(users), 0)

    def test_user_is_updated(self):
        mu1 = models.Account(uuid='10', username='u1', password_hash='p1', type='user')
        with Session(self.engine) as session, session.begin():
            session.add(mu1)
        updated_user = User('10', 'newu1', 'newp1')

        with self.assertRaises(ValueError):
            self.up.update(User('wrong_id', 'newu2', 'newp2'))

        self.up.update(updated_user)

        with Session(self.engine) as session, session.begin():
            users = session.query(models.Account).all()
            user = users[0]

            self.assertEqual(len(users), 1)
            self.assertEqual(user.uuid, '10')
            self.assertEqual(user.username, 'newu1')
            self.assertEqual(user.password_hash, 'newp1')
