import abc


class AdminProvider(abc.ABC):
    @abc.abstractmethod
    def get_admin(self, admin_id):
        pass

    @abc.abstractmethod
    def get_admins(self):
        pass

    @abc.abstractmethod
    def add_admin(self, admin):
        pass

    @abc.abstractmethod
    def add_admin_to_store(self, admin_id, store_id):
        pass

    @abc.abstractmethod
    def remove_admin(self, admin_id):
        pass

    @abc.abstractmethod
    def update(self, admin):
        pass

    @abc.abstractmethod
    def get_store_id(self, admin_id):
        pass
