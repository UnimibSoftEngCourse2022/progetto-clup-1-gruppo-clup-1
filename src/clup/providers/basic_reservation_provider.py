class BasicReservationProvider:
    def __init__(self):
        self.reservations = []

    def get_reservations(self):
        return self.reservations

    def add_reservation(self, reservation):
        if reservation.id in (r.id for r in self.reservations):
            raise ValueError('reservation id already present')

        self.reservations.append(reservation)

    # TODO: get_reservations_with_id(reservation_id)
