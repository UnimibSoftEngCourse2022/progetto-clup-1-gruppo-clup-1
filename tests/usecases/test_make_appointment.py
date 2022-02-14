import datetime
import unittest

from src.clup.entities.appointment import Appointment
from src.clup.usecases.make_appointment_usecase import MakeAppointmentUseCase


class MockAppointmentProvider:
    def __init__(self):
        self.appointments = {}

    def add_appointment(self, appointment):
        self.appointments[appointment.reservation_id] = appointment

    def get_appointment(self, reservation_id):
        return self.appointments[reservation_id]


class MockReservationProvider:
    def __init__(self):
        self.reservations = {}

    def add_reservation(self, res):
        pk = str(res.id) + str(res.aisle_id)
        self.reservations[pk] = res


class TestMakeAppointmentUsecase(unittest.TestCase):
    def test_appointment_correctly_added(self):
        mrp = MockReservationProvider()
        mapp = MockAppointmentProvider()
        mau = MakeAppointmentUseCase(reservation_provider=mrp, appointment_provider=mapp)
        user_id = 1
        aisle_ids = [1, 2, 3]
        date = datetime.datetime(2022, 2, 14, 10, 30)

        mau.execute(user_id, aisle_ids, 1, date)

        self.assertEqual(len(mrp.reservations), 3)
        self.assertEqual(len(mapp.appointments), 1)

    def test_appointment_with_wrong_date_raise(self):
        mrp = MockReservationProvider()
        mapp = MockAppointmentProvider()
        mau = MakeAppointmentUseCase(reservation_provider=mrp, appointment_provider=mapp)
        user_id = 1
        aisle_ids = [1, 2, 3]
        date = 5

        with self.assertRaises(ValueError):
            mau.execute(user_id, aisle_ids, 1, date)

    def test_add_appointment_has_correct_info_added(self):
        mrp = MockReservationProvider()
        mapp = MockAppointmentProvider()
        mau = MakeAppointmentUseCase(reservation_provider=mrp, appointment_provider=mapp)
        user_id = 1
        aisle_ids = [1, 2, 3]
        date = datetime.datetime(2022, 2, 14, 10, 30)

        res_id = mau.execute(user_id, aisle_ids, 1, date)

        appointment = Appointment(res_id, 1, date)

        self.assertEqual(appointment, mapp.get_appointment(res_id))
