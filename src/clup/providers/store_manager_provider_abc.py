import abc


class StoreManagerProvider(abc.ABC):
    @abc.abstractmethod
    def get_manager(self, manager_id):
        pass

    @abc.abstractmethod
    def get_store_managers(self):
        pass

    @abc.abstractmethod
    def create_new_store_manager(self, storemanager_id, secret):
        pass

    @abc.abstractmethod
    def get_id_from_secret(self, secret):
        pass

    @abc.abstractmethod
    def add_manager(self, store_manager):
        pass

    @abc.abstractmethod
    def delete_store_manager(self, manager_id):
        pass

    @abc.abstractmethod
    def update(self, manager_id):
        pass
