import abc


class AisleProvider(abc.ABC):
    @abc.abstractmethod
    def get_store_aisles_id(self, store_id):
        pass

    @abc.abstractmethod
    def add_aisle(self, store_id, aisle):
        pass

    @abc.abstractmethod
    def get_aisle(self, aisle_id):
        pass
