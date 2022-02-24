from src.clup.providers.abc.reservation_provider_abc \
    import ReservationProvider


class MockReservationProvider(ReservationProvider):
    def __init__(self, throws_on_add=False):
        self.reservations = []
        self.throws_on_add = throws_on_add

    def get_reservations(self):
        return self.reservations

    def get_reservations_with_id(self, reservation_id):
        raise NotImplementedError()

    def get_user_reservations(self, user_id):
        return [r for r in self.reservations if r.user_id == user_id]

    def get_user_id(self, reservation_id):
        raise NotImplementedError()

    def add_reservation(self, reservation):
        if self.throws_on_add:
            raise ValueError()
        self.reservations.append(reservation)

    def update_reservation(self, reservation):
        raise NotImplementedError()

    def delete_reservation(self, reservation_id):
        raise NotImplementedError()
