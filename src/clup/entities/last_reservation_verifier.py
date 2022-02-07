class LastReservationVerifier:
    def __init__(self, queue_provider, reservation_provider):
        self.queue_provider = queue_provider
        self.reservation_provider = reservation_provider

    def is_last(self, reservation_id):
        reservations = self.reservation_provider.get_reservations()
        reservation_with_given_id = [r for r in reservations if r.id == reservation_id]

        if not reservation_with_given_id :
            raise ValueError()

        for r in reservation_with_given_id:
            aisle_pool = self.queue_provider.get_active_pool(r.aisle_id)
            id_in_pool = r.id in aisle_pool
            if not id_in_pool:
                return False
        return True
