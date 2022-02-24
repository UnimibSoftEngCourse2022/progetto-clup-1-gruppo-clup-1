import unittest
from unittest.mock import create_autospec

from src.clup.entities.store_pool import StorePool
from src.clup.entities.user import User
from src.clup.providers.abc.user_provider_abc import UserProvider
from src.clup.providers.abc.reservation_provider_abc \
    import ReservationProvider
from src.clup.providers.abc.email_service_provider_abc import EmailServiceProvider
from src.clup.usecases.system.notify_enabled_reservation_owner \
    import NotifyEnabledReservationOwner


class TestNotifyEnabledReservationOwner(unittest.TestCase):
    def setUp(self):
        self.email_pvd = create_autospec(EmailServiceProvider)
        self.user_provider = create_autospec(UserProvider)
        self.reservation_provider = create_autospec(ReservationProvider)
        self.u = NotifyEnabledReservationOwner(self.reservation_provider,
                                               self.user_provider,
                                               self.email_pvd)

    def test_send_called_on_reservation_owner(self):
        u = User('uid', 'usermail', 'upw_hash')
        self.reservation_provider.get_user_id.return_value = 'uid'
        self.user_provider.get_user.return_value = u

        self.u.execute('reservation_id')

        self.email_pvd.send.assert_called_once_with(u.username, self.u.subject, self.u.content)

    def test_update_works_as_execute_but_using_a_store_pool(self):
        sp = StorePool()
        sp.last_added = 'reservation_id'
        u = User('uid', 'usermail', 'upw_hash')
        self.reservation_provider.get_user_id.return_value = 'uid'
        self.user_provider.get_user.return_value = u

        self.u.update(sp)

        self.email_pvd.send.assert_called_once_with(u.username, self.u.subject, self.u.content)
