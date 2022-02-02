class EnableReservationUseCase:
    def __init__(self, store_provider):
        self.store_provider = store_provider

    def execute(self, store_id, reservation):
        waiting_queue = self.store_provider.get_waiting_queue(store_id)
        active_pool = self.store_provider.get_active_pool(store_id)

        waiting_queue.remove(reservation)
        active_pool.add(reservation)
