import abc


class LaneProvider(abc.ABC):
    @abc.abstractmethod
    def get_waiting_queue(self, aisle_id):
        pass

    @abc.abstractmethod
    def get_aisle_pool(self, aisle_id):
        pass

    @abc.abstractmethod
    def get_store_pool(self, store_id):
        pass
