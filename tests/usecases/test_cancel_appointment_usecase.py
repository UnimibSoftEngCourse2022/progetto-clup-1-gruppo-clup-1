import unittest

from src.clup.entities.appointment import Appointment
from src.clup.entities.reservation import Reservation
from src.clup.usecases.user.cancel_appointment import CancelAppointment


class MockAppointmentProvider:
    def __init__(self):
        self.appointments = []

    def delete_appointment(self, res_id):
        for app in self.appointments:
            if app.reservation_id == res_id:
                self.appointments.remove(app)


class MockReservationProvider:
    def __init__(self):
        self.reservations = []

    def remove_reservation_with_user_check(self, reservation_id, user_id):
        self.reservations = [r for r in self.reservations
                             if r.id != reservation_id and r.user_id != user_id]


class TestCancelAppointmentUseCase(unittest.TestCase):
    def setUp(self):
        self.mrp = MockReservationProvider()
        self.maip = MockAppointmentProvider()
        res1_id = 'reservation1'
        res2_id = 'reservation2'

        self.a1 = Appointment(reservation_id=res1_id,
                              date_time=0,
                              store_id='store')
        self.a2 = Appointment(reservation_id=res2_id,
                              date_time=0,
                              store_id='store')
        self.maip.appointments = [self.a1, self.a2]

        self.r11 = Reservation(aisle_id='aisle1',
                               user_id='user1',
                               id=res1_id)
        self.r12 = Reservation(aisle_id='aisle2',
                               user_id='user1',
                               id=res1_id)
        self.r21 = Reservation(aisle_id='aisle1',
                               user_id='user2',
                               id=res2_id)
        self.r22 = Reservation(aisle_id='aisle2',
                               user_id='user2',
                               id=res2_id)
        self.mrp.reservations = [self.r11, self.r12, self.r21, self.r22]

    def test_correct_reservations_removed(self):
        cau = CancelAppointment(self.maip, self.mrp)
        cau.execute('user1', 'reservation1')
        self.assertTrue(self.a1 not in self.maip.appointments)
        self.assertTrue(self.a2 in self.maip.appointments)
        self.assertTrue(self.r11 not in self.mrp.reservations)
        self.assertTrue(self.r12 not in self.mrp.reservations)
        self.assertTrue(self.r21 in self.mrp.reservations)
        self.assertTrue(self.r22 in self.mrp.reservations)
