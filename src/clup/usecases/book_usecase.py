import uuid

from src.clup.entities.reservation import Reservation


class BookUseCase:
    def __init__(self, queue_provider, reservation_provider):
        self.queue_provider = queue_provider
        self.reservation_provider = reservation_provider

    def execute(self, store_id, user_id):
        reservation_id = str(uuid.uuid1())

        reservation = Reservation(reservation_id, store_id, user_id)
        self.reservation_provider.add_reservation(reservation)
        waiting_queue = self.queue_provider.get_waiting_queue(store_id)
        waiting_queue.push(reservation)

        return reservation
