import abc


class StoreProvider(abc.ABC):
    @abc.abstractmethod
    def get_stores(self):
        pass

    @abc.abstractmethod
    def get_store(self, store_id):
        pass

    @abc.abstractmethod
    def add_store(self, store):
        pass

    @abc.abstractmethod
    def update_store(self, store):
        pass

    @abc.abstractmethod
    def delete_store(self, store_id):
        pass

    @abc.abstractmethod
    def get_store_from_manager_id(self, manager_id):
        pass
