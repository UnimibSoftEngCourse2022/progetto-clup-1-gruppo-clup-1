import abc


class ReservationProvider(abc.ABC):
    @abc.abstractmethod
    def get_reservations(self):
        pass

    @abc.abstractmethod
    def add_reservation(self, reservation):
        pass

    @abc.abstractmethod
    def update_reservation(self, reservation):
        pass

    @abc.abstractmethod
    def delete_reservation(self, reservation_id):
        pass
