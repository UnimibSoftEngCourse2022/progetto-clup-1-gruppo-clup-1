import unittest
from unittest.mock import create_autospec, call

from src.clup.entities.user import User
from src.clup.entities.admin import Admin
from src.clup.entities.store_manager import StoreManager
from src.clup.providers.email_service_provider_abc import EmailServiceProvider
from src.clup.usecases.notify_enabled_accounts import NotifyEnabledAccounts


class TestNotifyEnabledAccounts(unittest.TestCase):
    def setUp(self):
        self.email_pvd = create_autospec(EmailServiceProvider)
        self.u = NotifyEnabledAccounts(self.email_pvd)

    def test_no_send_on_empty_account_list(self):
        self.u.execute([])

        self.email_pvd.send.assert_not_called()

    def test_send_called_on_each_account_username(self):
        u = User('uid', 'usermail', 'upw_hash')
        a = Admin('aid', 'adminmail', 'apw_hash')
        m = StoreManager('mid', 'managermail', 'mpw_hash')

        self.u.execute([u, a, m])

        expected_calls = [call(u.username, self.u.subject, self.u.content),
                          call(a.username, self.u.subject, self.u.content),
                          call(m.username, self.u.subject, self.u.content),]
        self.email_pvd.send.assert_has_calls(expected_calls, any_order=True)
        self.assertEqual(self.email_pvd.send.call_count, 3)
