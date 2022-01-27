import uuid


def book(market_id, queue):
    reservation_id = uuid.uuid1()
    reservation = (reservation_id, market_id)
    updated_queue = queue + (reservation_id,)
    return reservation, updated_queue


class BookUseCase:
    def __init__(self, store_provider):
        self.store_provider = store_provider

    def book(self, store_id):
        queue = self.store_provider.get_queue(store_id)
        reservation_id = uuid.uuid1()
        updated_queue = queue + (reservation_id,)
        self.store_provider.save_queue(store_id, updated_queue)
        return reservation_id

    def consume(self, reservation_id, store_id):
        found = False
        queue = self.store_provider.get_queue(store_id)
        updated_queue = []
        for reservation in queue:
            if reservation != reservation_id:
                updated_queue.append(reservation)
            else:
                found = True

        self.store_provider.save_queue(store_id, updated_queue)

        return found



