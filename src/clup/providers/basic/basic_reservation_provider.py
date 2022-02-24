from src.clup.providers.abc.reservation_provider_abc \
    import ReservationProvider


class BasicReservationProvider(ReservationProvider):
    def __init__(self):
        self.reservations = []

    def get_reservations(self):
        return self.reservations

    def get_reservations_with_id(self, reservation_id):
        raise NotImplementedError()

    def get_user_reservations(self, user_id):
        raise NotImplementedError()

    def get_user_id(self, reservation_id):
        raise NotImplementedError()

    def add_reservation(self, reservation):
        # if reservation.id in (r.id for r in self.reservations):
        #     raise ValueError('reservation id already present')
        self.reservations.append(reservation)

    def update_reservation(self, reservation):
        raise NotImplementedError()

    def delete_reservation(self, reservation_id):
        raise NotImplementedError()
