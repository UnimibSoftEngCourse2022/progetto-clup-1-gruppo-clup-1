import abc


class UserProvider(abc.ABC):
    @abc.abstractmethod
    def get_user(self, user_id):
        pass

    @abc.abstractmethod
    def get_users(self):
        pass

    @abc.abstractmethod
    def add_user(self, user):
        pass

    @abc.abstractmethod
    def remove_user(self, user_id):
        pass

    @abc.abstractmethod
    def update(self, user):
        pass
