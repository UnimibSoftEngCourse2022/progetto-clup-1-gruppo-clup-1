import unittest
from unittest.mock import create_autospec

from werkzeug.security import generate_password_hash, check_password_hash

from src.clup.entities.exceptions import AuthError
from src.clup.entities.user import User
from src.clup.entities.admin import Admin
from src.clup.entities.store_manager import StoreManager
from src.clup.providers.abc.user_provider_abc import UserProvider
from src.clup.providers.abc.admin_provider_abc import AdminProvider
from src.clup.providers.abc.store_manager_provider_abc import StoreManagerProvider
from src.clup.usecases.auth.change_password import ChangePassword


class TestChangePassword(unittest.TestCase):
    def setUp(self):
        self.up = create_autospec(UserProvider)
        self.ap = create_autospec(AdminProvider)
        self.smp = create_autospec(StoreManagerProvider)
        self.u = ChangePassword(self.up, self.ap, self.smp)

    def test_change_password_for_users(self):
        pwd = 'usr_pwd'
        pwd_hash = generate_password_hash(pwd)
        user = User('uid', 'usr', pwd_hash)
        new_pwd = 'new_pwd'
        self.up.get_user.return_value = user

        self.u.execute(user.id, pwd, new_pwd)

        self.up.update.assert_called_once()
        new_user = self.up.update.call_args.args[0]
        self.assertEqual(new_user.id, user.id)
        self.assertEqual(new_user.username, user.username)
        self.assertTrue(check_password_hash(new_user.password_hash, new_pwd))

    def test_change_password_for_admins(self):
        pwd = 'admin_pwd'
        pwd_hash = generate_password_hash(pwd)
        admin = Admin('aid', 'admin', pwd_hash)
        new_pwd = 'new_pwd'
        self.up.get_user.side_effect = ValueError()
        self.ap.get_admin.return_value = admin

        self.u.execute(admin.id, pwd, new_pwd)

        self.ap.update.assert_called_once()
        new_admin = self.ap.update.call_args.args[0]
        self.assertEqual(new_admin.id, admin.id)
        self.assertEqual(new_admin.username, admin.username)
        self.assertTrue(check_password_hash(new_admin.password_hash, new_pwd))

    def test_change_password_for_store_managers(self):
        pwd = 'store_manager_pwd'
        pwd_hash = generate_password_hash(pwd)
        store_manager = StoreManager('aid', 'store_manager', pwd_hash)
        new_pwd = 'new_pwd'
        self.up.get_user.side_effect = ValueError()
        self.ap.get_admin.side_effect = ValueError()
        self.smp.get_manager.return_value = store_manager

        self.u.execute(store_manager.id, pwd, new_pwd)

        self.smp.update.assert_called_once()
        new_store_manager = self.smp.update.call_args.args[0]
        self.assertEqual(new_store_manager.id, store_manager.id)
        self.assertEqual(new_store_manager.username, store_manager.username)
        self.assertTrue(check_password_hash(new_store_manager.password_hash, new_pwd))

    def test_unexistent_id_throws(self):
        self.up.get_user.side_effect = ValueError()
        self.ap.get_admin.side_effect = ValueError()
        self.smp.get_manager.side_effect = ValueError()

        with self.assertRaises(ValueError):
            self.u.execute('account_id', 'old_pwd', 'new_pwd')

    def test_empty_or_none_new_password_throws(self):
        user = User('uid', 'usr', 'pwd_hash')
        self.up.get_user.return_value = user

        with self.assertRaises(ValueError):
            self.u.execute('account_id', 'old_pwd', '')

        with self.assertRaises(ValueError):
            self.u.execute('account_id', 'old_pwd', None)

    def test_wrong_user_password_throws(self):
        pwd = 'usr_pwd'
        pwd_hash = generate_password_hash(pwd)
        user = User('uid', 'usr', pwd_hash)
        self.up.get_user.return_value = user

        with self.assertRaises(AuthError):
            self.u.execute(user.id, 'wrong_pwd', 'new_pwd')

    def test_wrong_admin_password_throws(self):
        pwd = 'admin_pwd'
        pwd_hash = generate_password_hash(pwd)
        admin = Admin('aid', 'admin', pwd_hash)
        self.up.get_user.side_effect = ValueError()
        self.ap.get_admin.return_value = admin

        with self.assertRaises(AuthError):
            self.u.execute(admin.id, 'wrong_pwd', 'new_pwd')

    def test_wrong_store_manager_password_throws(self):
        pwd = 'store_manager_pwd'
        pwd_hash = generate_password_hash(pwd)
        store_manager = StoreManager('aid', 'store_manager', pwd_hash)
        self.up.get_user.side_effect = ValueError()
        self.ap.get_admin.side_effect = ValueError()
        self.smp.get_manager.return_value = store_manager

        with self.assertRaises(AuthError):
            self.u.execute(store_manager.id, 'wrong_pwd', 'new_pwd')
