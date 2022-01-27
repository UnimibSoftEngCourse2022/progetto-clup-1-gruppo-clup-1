import uuid


class BookUseCase:
    def __init__(self, store_provider):
        self.store_provider = store_provider

    def book(self, store_id):
        queue = self.store_provider.get_queue(store_id)
        reservation_id = uuid.uuid1()
        updated_queue = queue + (reservation_id,)
        self.store_provider.save_queue(store_id, updated_queue)
        reservation = (reservation_id, store_id)
        return reservation

    def consume(self, reservation):
        reservation_id, store_id = reservation
        queue = self.store_provider.get_queue(store_id)
        found = reservation_id in queue
        updated_queue = [res for res in queue if res != reservation_id]
        self.store_provider.save_queue(store_id, updated_queue)

        return found



