import abc


class StoreProvider(abc.ABC):
    @abc.abstractmethod
    def get_stores(self):
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
