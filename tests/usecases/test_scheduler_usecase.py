import datetime
import unittest

from src.clup.usecases.make_appointment_usecase import MakeAppointmentUseCase
from src.clup.usecases.scheduler_usecase import SchedulerUseCase
from tests.usecases.mock_lane_provider import MockLaneProvider


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

    def add_reservation(self, res):
        self.reservations.append(res)

    def get_reservations_with_id(self, reservation_id):
        return [res for res in self.reservations if res.id == reservation_id]


class TestSchedulerUsecase(unittest.TestCase):
    def test_scheduler_do_as_expected(self):
        mapp = MockAppointmentProvider()
        mrp = MockReservationProvider()
        mlp = MockLaneProvider()
        su = SchedulerUseCase(mapp, mrp, mlp)
        mau = MakeAppointmentUseCase(reservation_provider=mrp, appointment_provider=mapp)
        user_id = 'user'
        aisles = [1, 2, 3]
        store_id = 'store'

        date = datetime.datetime(2022, 2, 14, 12, 30)
        reservation_id = mau.execute(
            user_id=user_id,
            aisle_ids=aisles,
            store_id=store_id,
            date=date
        )

        su.execute(date)

        # se non ci sono dovrebbe crashare
        mlp.get_waiting_queue(1).pop()
        mlp.get_waiting_queue(2).pop()
        mlp.get_waiting_queue(3).pop()
