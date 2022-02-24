import unittest

from src.clup.entities.admin import Admin
from src.clup.usecases.admin.load_admin_usecase import LoadAdminUseCase


class MockAdminProvider:
    def __init__(self):
        self.admins = []

    def get_admins(self):
        return self.admins


class TestLoadAdminUsecase(unittest.TestCase):
    def setUp(self):
        self.admin_provider = MockAdminProvider()
        self.u = LoadAdminUseCase(self.admin_provider)

    def test_admin_is_returned(self):
        u = Admin('1', 'tizio', 'caio')
        self.admin_provider.admins.append(u)

        admin = self.u.execute('1')

        self.assertEqual(admin.id, '1')
        self.assertEqual(admin.username, 'tizio')
        self.assertEqual(admin.password_hash, 'caio')

    def test_unexistent_admin_id_throws(self):
        with self.assertRaises(ValueError):
            self.u.execute('1')

    def test_admin_with_id_is_returned(self):
        u1 = Admin('1', 'tizio', 'caio')
        u2 = Admin('2', 'pluto', 'paperino')
        self.admin_provider.admins.append(u1)
        self.admin_provider.admins.append(u2)

        admin = self.u.execute('2')

        self.assertEqual(admin.id, '2')
        self.assertEqual(admin.username, 'pluto')
        self.assertEqual(admin.password_hash, 'paperino')
