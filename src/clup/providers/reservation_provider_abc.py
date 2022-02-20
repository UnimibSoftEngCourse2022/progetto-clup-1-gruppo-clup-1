import abc


class ReservationProvider(abc.ABC):
    @abc.abstractmethod
    def get_reservations(self):
        pass

    @abc.abstractmethod
    def get_reservations_with_id(self, reservation_id):
        pass

    @abc.abstractmethod
    def get_user_reservations(self, user_id):
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
