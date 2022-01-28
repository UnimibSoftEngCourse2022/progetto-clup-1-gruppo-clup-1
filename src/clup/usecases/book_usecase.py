import uuid


class BookUseCase:
    def __init__(self, store_provider, reservation_provider):
        self.store_provider = store_provider
        self.reservation_provider = reservation_provider

    def execute(self, store_id, user_id):
        queue = self.store_provider.get_queue(store_id)

        reservation_id = str(uuid.uuid1())
        updated_queue = queue + (reservation_id,)
        self.store_provider.set_queue(store_id, updated_queue)

        reservation = reservation_id, store_id, user_id
        self.reservation_provider.add_reservation(reservation)

        return reservation

