import uuid
from datetime import datetime

from src.clup.entities.reservation import Reservation


class MakeAppointmentUseCase:
    def __init__(self, reservation_provider, appointment_provider):
        self.reservation_provider = reservation_provider
        self.appointment_provider = appointment_provider

    def execute(self, user_id, aisle_ids, date):
        reservation_id = str(uuid.uuid1())
        if type(date) is not datetime:
            raise ValueError("Not a correct date")

        self.appointment_provider.add_appointment(reservation_id, date)

        for aisle_id in aisle_ids:
            res = Reservation(reservation_id, aisle_id, user_id)
            self.reservation_provider.add_reservation(res)

        return reservation_id