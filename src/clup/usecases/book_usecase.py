import uuid


class BookUseCase:
    def __init__(self, queue_provider, reservation_provider):
        self.queue_provider = queue_provider
        self.reservation_provider = reservation_provider

    def execute(self, store_id, user_id):
        queue = self.queue_provider.get_queue(store_id)

        reservation_id = str(uuid.uuid1())
        self.queue_provider.add_to_queue(store_id, reservation_id)

        reservation = reservation_id, store_id, user_id
        self.reservation_provider.add_reservation(reservation)

        return reservation

