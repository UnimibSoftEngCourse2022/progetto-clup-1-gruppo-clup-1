import abc


class AisleProvider(abc.ABC):
    @abc.abstractmethod
    def get_aisles(self):
        pass

    @abc.abstractmethod
    def get_aisle(self, aisle_id):
        pass

    @abc.abstractmethod
    def get_store_aisle_ids(self, store_id):
        pass

    @abc.abstractmethod
    def add_aisle(self, store_id, aisle):
        pass

    @abc.abstractmethod
    def get_store_aisles(self, store_id):
        pass
