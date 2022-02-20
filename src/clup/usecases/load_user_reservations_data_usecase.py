class LoadUserReservationsDataUseCase:
    def __init__(self, reservation_provider, store_provider, aisle_provider):
        self.reservation_provider = reservation_provider
        self.store_provider = store_provider
        self.aisle_provider = aisle_provider

    def execute(self, user_id):
        user_reservations = \
            self.reservation_provider.get_user_reservations(user_id)
        reservations_aisle_ids = [r.aisle_id for r in user_reservations]

        stores = self.store_provider.get_stores()
        data = []
        for store in stores:
            store_reserved_aisles = []
            store_aisles = self.aisle_provider.get_store_aisles(store.id)
            for aisle in store_aisles:
                if aisle.id in reservations_aisle_ids:
                    store_reserved_aisles.append(aisle)
            if len(store_reserved_aisles) > 0:
                data.append((store, store_reserved_aisles))

        return data
