import uuid

from src.clup.entities.exceptions import MaxCapacityReachedError
from src.clup.entities.reservation import Reservation


class MakeReservationUseCase:
    def __init__(self, queue_provider, reservation_provider):
        self.queue_provider = queue_provider
        self.reservation_provider = reservation_provider

    def execute(self, user_id, store_id, aisle_ids):
        reservation_id = str(uuid.uuid1())

        for aisle_id in aisle_ids:
            reservation = Reservation(reservation_id, aisle_id, user_id)
            self.reservation_provider.add_reservation(reservation)

        active_pool = self.queue_provider.get_active_pool(store_id)
        try:
            active_pool.add(reservation.id)
        except MaxCapacityReachedError:
            waiting_queue = self.queue_provider.get_waiting_queue(store_id)
            waiting_queue.push(reservation.id)

        return reservation_id
