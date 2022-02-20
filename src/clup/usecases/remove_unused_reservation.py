class RemoveUnusedReservation:
    def __init__(self, store_provider, lane_provider, reservation_provider):
        self.store_provider = store_provider
        self.lane_provider = lane_provider
        self.reservation_provider = reservation_provider

    def execute(self):
        reservations_in_stores_pools = []
        for store in self.store_provider.get_stores():
            store_pool = self.lane_provider.get_store_pool(store.id)
            reservation = store_pool.enabled
            reservations_in_stores_pools.extend(reservation)
        try:
            with open('./active_reservations.txt', 'r') as file:
                old_reservations = []
                for line in file:
                    old_reservations.append(line.strip())
        except FileNotFoundError:
            old_reservations = []

        to_be_removed = []
        if len(old_reservations) != 0:
            for old_res in old_reservations:
                if old_res in reservations_in_stores_pools:
                    to_be_removed.append(old_res)
                    reservations_in_stores_pools.remove(old_res)

        for res in to_be_removed:
            aisle_id_of_res = [r.aisle_id for r in self.reservation_provider.get_reservations_with_id(res)]
            for aisle_id in aisle_id_of_res:
                aisle_pool = self.lane_provider.get_aisle_pool(aisle_id)
                aisle_pool.invalidate(res)
            store_id = self.reservation_provider.get_store_from_reservation_id(res)
            store_pool = self.lane_provider.get_store_pool(store_id)
            store_pool.enabled.remove(res)

        with open('./active_reservations.txt', 'w') as file:
            for res in reservations_in_stores_pools:
                file.write(f'{res}\n')