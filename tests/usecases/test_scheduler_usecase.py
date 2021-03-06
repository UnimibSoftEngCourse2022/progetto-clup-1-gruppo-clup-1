import datetime
import unittest

from src.clup.entities.aisle import Aisle
from src.clup.usecases.user.make_appointment import MakeAppointment
from src.clup.usecases.system.enable_scheduled_appointments import Scheduler
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

    def delete_appointment(self, appointment_id):
        self.appointments[appointment_id] = None


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


class TestSchedulerUsecase(unittest.TestCase):
    def test_scheduler_do_as_expected(self):
        mapp = MockAppointmentProvider()
        mrp = MockReservationProvider()
        mlp = MockLaneProvider()
        maip = MockAisleProvider()
        aisle1 = Aisle(1, 'aisle1', [], 10)
        aisle2 = Aisle(2, 'aisle2', [], 10)
        aisle3 = Aisle(3, 'aisle3', [], 10)
        maip.add_aisle(aisle1)
        maip.add_aisle(aisle2)
        maip.add_aisle(aisle3)

        su = Scheduler(mapp, mrp, mlp)
        mau = MakeAppointment(reservation_provider=mrp, appointment_provider=mapp, aisle_provider=maip)
        user_id = 'user'
        aisles_ids = [1, 2, 3]
        store_id = 'store'

        date = datetime.datetime(2022, 2, 14, 12, 30)
        mau.execute(
            user_id=user_id,
            aisle_ids=aisles_ids,
            store_id=store_id,
            date=date
        )

        su.execute(datetime.datetime(date.year, date.month, date.day, date.hour))

        # se non ci sono dovrebbe crashare
        mlp.get_waiting_queue(1).pop()
        mlp.get_waiting_queue(2).pop()
        mlp.get_waiting_queue(3).pop()
