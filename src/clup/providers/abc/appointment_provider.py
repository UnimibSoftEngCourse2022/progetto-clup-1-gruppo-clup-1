import abc


class AppointmentProvider(abc.ABC):
    @abc.abstractmethod
    def add_appointment(self, appointment):
        pass

    @abc.abstractmethod
    def get_appointments(self):
        pass

    @abc.abstractmethod
    def get_user_appointments(self, user_id):
        pass

    @abc.abstractmethod
    def get_appointment(self, reservation_id):
        pass

    @abc.abstractmethod
    def delete_appointment(self, reservation_id):
        pass
