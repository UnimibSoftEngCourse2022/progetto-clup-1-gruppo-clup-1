class FreeReservationUseCase:
    def __init__(self, lane_provider, reservation_provider):
        self.lane_provider = lane_provider
        self.reservation_provider = reservation_provider

    def execute(self, store_id, reservation_id):
        involved_aisle_ids = self._get_involved_aisle_ids(reservation_id)
        for aisle_id in involved_aisle_ids:
            aisle_pool = self.lane_provider.get_aisle_pool(aisle_id)
            aisle_pool.free()

        store_pool = self.lane_provider.get_store_pool(store_id)
        store_pool.free(reservation_id)

        for aisle_id in involved_aisle_ids:
            queue = self.lane_provider.get_waiting_queue(aisle_id)
            if len(queue) <= 0:
                continue

            waiting_reservation_id = queue.pop()
            aisle_pool = self.lane_provider.get_aisle_pool(aisle_id)
            aisle_pool.add(waiting_reservation_id)

            if self._is_in_all_involved_pools(waiting_reservation_id):
                store_pool.add(waiting_reservation_id)

    def _get_involved_aisle_ids(self, reservation_id):
        reservations = self.reservation_provider.get_reservations()
        filtered = [r for r in reservations if r.id == reservation_id]
        aisle_ids = [r.aisle_id for r in filtered]
        return aisle_ids

    def _is_in_all_involved_pools(self, reservation_id):
        aisle_ids = self._get_involved_aisle_ids(reservation_id)
        for aisle_id in aisle_ids:
            aisle_pool = self.lane_provider.get_aisle_pool(aisle_id)
            if reservation_id not in aisle_pool:
                return False
        return True
        
