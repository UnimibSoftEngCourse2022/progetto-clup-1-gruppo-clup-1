class ConsumeReservationUseCase:
    def __init__(self, queue_provider):
        self.queue_provider = queue_provider

    def execute(self, store_id, reservation_id):
        pool = self.queue_provider.get_aisle_pool(store_id)
        pool.consume(reservation_id)
