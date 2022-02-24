class ConsumeReservationUseCase:
    def __init__(self, lane_provider, reservation_provider):
        self.lane_provider = lane_provider
        self.reservation_provider = reservation_provider

    def execute(self, store_id, reservation_id):
        reservations = self.reservation_provider.get_reservations()
        filtered = [r for r in reservations if r.id == reservation_id]
        if not filtered:
            raise ValueError("reservation_id not existing")

        for r in filtered:
            aisle_pool = self.lane_provider.get_aisle_pool(r.aisle_id)
            aisle_pool.consume(reservation_id)

        store_pool = self.lane_provider.get_store_pool(store_id)
        store_pool.consume(reservation_id)
