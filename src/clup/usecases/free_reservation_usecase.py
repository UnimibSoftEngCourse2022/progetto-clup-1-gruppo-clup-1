class FreeReservationUseCase:
    def __init__(self, queue_provider):
        self.queue_provider = queue_provider

    def execute(self, store_id):
        pool = self.queue_provider.get_active_pool(store_id)
        pool.free()

        queue = self.queue_provider.get_waiting_queue(store_id)
        if len(queue) > 0:
            reservation = queue.pop()
            pool.add(reservation)
