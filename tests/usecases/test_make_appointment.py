import datetime
import unittest

from src.clup.entities.aisle import Aisle
from src.clup.entities.appointment import Appointment
from src.clup.usecases.make_appointment_usecase import MakeAppointmentUseCase


class MockAppointmentProvider:
    def __init__(self):
        self.appointments = {}

    def add_appointment(self, appointment):
        self.appointments[appointment.reservation_id] = appointment

    def get_appointment(self, reservation_id):
        return self.appointments[reservation_id]

    def get_appointments(self):
        return self.appointments.values()


class MockReservationProvider:
    def __init__(self):
        self.reservations = []
        self.store_aisle = []

    def add_reservation(self, res):
        self.reservations.append(res)

    def get_reservations_with_id(self, reservation_id):
        return [res for res in self.reservations if res.id == reservation_id]

    def reservation_for_aisles_of_same_store(self, store_id, aisle_ids):
        for store, aisle in self.store_aisle:
            for aisle_id in aisle_ids:
                if aisle == aisle_id and store != store_id:
                    raise ValueError


class MockAisleProvider:
    def __init__(self):
        self.aisles = {}

    def get_aisles(self):
        return self.aisles.values()

    def add_aisle(self, aisle):
        self.aisles[aisle.id] = aisle

    def get_aisle(self, aisle_id):
        return self.aisles[aisle_id]


class TestMakeAppointmentUsecase(unittest.TestCase):
    def setUp(self):
        self.maip = MockAisleProvider()
        aisle1 = Aisle(1, 'aisle1', [], 100)
        aisle2 = Aisle(2, 'aisle2', [], 100)
        aisle3 = Aisle(3, 'aisle3', [], 100)
        self.maip.add_aisle(aisle1)
        self.maip.add_aisle(aisle2)
        self.maip.add_aisle(aisle3)

    def test_appointment_correctly_added(self):
        mrp = MockReservationProvider()
        mapp = MockAppointmentProvider()
        mau = MakeAppointmentUseCase(reservation_provider=mrp, appointment_provider=mapp, aisle_provider=self.maip)
        user_id = 1
        aisle_ids = [1, 2, 3]
        date = datetime.datetime(2022, 2, 14, 10, 30)

        mau.execute(user_id, aisle_ids, 1, date)

        self.assertEqual(len(mrp.reservations), 3)
        self.assertEqual(len(mapp.appointments), 1)

    def test_appointment_with_wrong_date_raise(self):
        mrp = MockReservationProvider()
        mapp = MockAppointmentProvider()
        mau = MakeAppointmentUseCase(reservation_provider=mrp, appointment_provider=mapp, aisle_provider=self.maip)
        user_id = 1
        aisle_ids = [1, 2, 3]
        date = 5

        with self.assertRaises(ValueError):
            mau.execute(user_id, aisle_ids, 1, date)

    def test_add_appointment_has_correct_info_added(self):
        mrp = MockReservationProvider()
        mapp = MockAppointmentProvider()
        mau = MakeAppointmentUseCase(reservation_provider=mrp, appointment_provider=mapp, aisle_provider=self.maip)
        user_id = 1
        aisle_ids = [1, 2, 3]
        date = datetime.datetime(2022, 2, 14, 10, 30)

        res_id = mau.execute(user_id, aisle_ids, 1, date)

        appointment = Appointment(res_id, 1, date)

        self.assertEqual(appointment.reservation_id, mapp.get_appointment(res_id).reservation_id)
