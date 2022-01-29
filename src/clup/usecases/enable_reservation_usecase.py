class EnableReservationUseCase:
    def __init__(self, store_provider):
        self.store_provider = store_provider

    def execute(self, reservation):
        reservation_id, store_id = reservation
        queue = self.store_provider.get_queue(store_id)
        found = reservation_id in queue
        updated_queue = tuple([res for res in queue if res != reservation_id])
        self.store_provider.set_queue(store_id, updated_queue)

        return found
