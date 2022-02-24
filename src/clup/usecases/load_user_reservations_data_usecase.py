from collections import defaultdict


class LoadUserReservationsDataUseCase:
    def __init__(self, reservation_provider, store_provider, 
                 aisle_provider, appointment_provider):
        self.reservation_provider = reservation_provider
        self.store_provider = store_provider
        self.aisle_provider = aisle_provider
        self.appointment_provider = appointment_provider

    def execute(self, user_id):
        user_reservations = \
            self.reservation_provider.get_user_reservations(user_id)

        user_appointments = \
            self.appointment_provider.get_user_appointments(user_id)

        appointment_ids = [a.reservation_id for a in user_appointments]
        user_reservations = [r 
                             for r in user_reservations 
                             if r.id not in appointment_ids]

        reservation_with_aisle_ids = defaultdict(list)
        for r in user_reservations:
            reservation_with_aisle_ids[r.id].append(r.aisle_id)

        data = []
        for r_id, aisle_ids in reservation_with_aisle_ids.items():
            aisles = [self.aisle_provider.get_aisle(id) for id in aisle_ids]
            store = self._get_store(aisle_ids[0])
            data.append((r_id, store, aisles))

        return data

    def _get_store(self, aisle_id):
        stores = self.store_provider.get_stores()
        for store in stores:
            store_aisles = self.aisle_provider.get_store_aisles(store.id)
            if aisle_id in [a.id for a in store_aisles]:
                return store
