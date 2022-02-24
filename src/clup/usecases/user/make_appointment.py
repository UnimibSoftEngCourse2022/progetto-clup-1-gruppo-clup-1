import uuid
from collections import Counter
from datetime import datetime

from src.clup.entities.appointment import Appointment
from src.clup.entities.exceptions import MaxCapacityReachedError
from src.clup.entities.reservation import Reservation


class MakeAppointment:
    def __init__(self, reservation_provider, appointment_provider, aisle_provider):
        self.reservation_provider = reservation_provider
        self.appointment_provider = appointment_provider
        self.aisle_provider = aisle_provider

    def execute(self, user_id, aisle_ids, store_id, date):
        try:
            self.reservation_provider.reservation_for_aisles_of_same_store(store_id, aisle_ids)
        except ValueError:
            print("INCOHERENT AISLE")
            raise

        reservation_id = str(uuid.uuid1())

        if type(date) is not datetime:
            raise ValueError("Not a correct date")
        date_to_hour = datetime(year=date.year, month=date.month, day=date.day, hour=date.hour)

        if not self.check_enough_spaces_in_aisles(aisle_ids, date_to_hour):
            raise MaxCapacityReachedError()

        appointment = Appointment(reservation_id, store_id, date_to_hour)
        self.appointment_provider.add_appointment(appointment)

        for aisle_id in aisle_ids:
            res = Reservation(reservation_id, aisle_id, user_id)
            self.reservation_provider.add_reservation(res)

        return reservation_id

    def check_enough_spaces_in_aisles(self, aisle_ids, date):
        enough_space = True
        appointments_in_same_date = [a for a in self.appointment_provider.get_appointments() if
                                     a.date_time.year == date.year and
                                     a.date_time.month == date.month and
                                     a.date_time.day == date.day and
                                     a.date_time.hour == date.hour]

        res_same_date_same_aisles = []
        for appointment in appointments_in_same_date:
            aisle_ids_filtered = [r.aisle_id for r in
                                  self.reservation_provider.get_reservations_with_id(appointment.reservation_id)
                                  if r.aisle_id in aisle_ids]

            res_same_date_same_aisles.extend(aisle_ids_filtered)
        count_people_in_aisle = Counter(res_same_date_same_aisles)
        for aisle_id in aisle_ids:
            capacity = self.aisle_provider.get_aisle(aisle_id).capacity
            if count_people_in_aisle[aisle_id] > capacity - 1:
                enough_space = False
        return enough_space
