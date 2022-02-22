import unittest

from werkzeug.security import check_password_hash, generate_password_hash

from src.clup.entities.admin import Admin
from src.clup.entities.store_manager import StoreManager
from src.clup.entities.user import User
from src.clup.providers.store_manager_provider_abc \
    import StoreManagerProvider
from src.clup.usecases.generic_login_usecase import GenericLoginUsecase


class MockUserProvider:
    def __init__(self):
        self.users = {}

    def add_user(self, user):
        self.users[user.id] = user

    def get_users(self):
        return self.users.values()


class MockAdminProvider:
    def __init__(self):
        self.admins = {}

    def add_admin(self, admin):
        self.admins[admin.id] = admin

    def get_admins(self):
        return self.admins.values()


class MockStoreManagerProvider(StoreManagerProvider):
    def __init__(self):
        self.store_managers = {}
        self.store_manager_stores = []

    def get_store_managers(self):
        return self.store_managers.values()

    def create_new_store_manager(self, sm_id, secret):
        raise NotImplementedError()

    def get_id_from_secret(self, secret):
        raise NotImplementedError()

    def add_manager(self, manager):
        self.store_managers[manager.id] = manager

    def delete_store_manager(self, sm_id, secret):
        raise NotImplementedError()

    def get_manager(self, sm_id, secret):
        raise NotImplementedError()


class TestGenericLoginUsecase(unittest.TestCase):
    def setUp(self):
        self.up = MockUserProvider()
        self.ap = MockAdminProvider()
        self.smp = MockStoreManagerProvider()
        self.u = GenericLoginUsecase(self.ap, self.up, self.smp)

    def test_generic_login_works_with_user(self):
        password = 'upwd'
        pw_hashed = generate_password_hash(password)
        user = User('uid', 'name', pw_hashed)
        self.up.add_user(user)

        _, logged_type = self.u.execute(user.username, password)
        is_user_logged = logged_type == 'user'

        self.assertTrue(is_user_logged)

    def test_generic_login_works_with_admin(self):
        apassword = 'apwd'
        apw_hashed = generate_password_hash(apassword)
        admin = Admin('aid', 'aname', apw_hashed)
        self.ap.add_admin(admin)

        _, logged_type = self.u.execute(admin.username, apassword)
        is_admin_logged = logged_type == 'admin'

        self.assertTrue(is_admin_logged)

    def test_login_works_with_store_manager(self):
        mpassword = 'mpwd'
        mpw_hashed = generate_password_hash(mpassword)
        manager = StoreManager('mid', 'mname', mpw_hashed)
        self.smp.add_manager(manager)

        _, logged_type = self.u.execute(manager.username, mpassword)
        is_sm_logged = logged_type == 'store_manager'

        self.assertTrue(is_sm_logged)

    def test_login_with_wrong_credentials_raise_exception(self):
        upassword = 'upwd'
        upw_hashed = generate_password_hash(upassword)
        apassword = 'apwd'
        apw_hashed = generate_password_hash(apassword)
        user = User('uid', 'uname', upw_hashed)
        admin = Admin('aid', 'aname', apw_hashed)
        self.up.add_user(user)
        self.ap.add_admin(admin)

        with self.assertRaises(ValueError):
            self.u.execute(user.username, 'wrong_pwd')
        with self.assertRaises(ValueError):
            self.u.execute(admin.username, 'wrong_pwd')
