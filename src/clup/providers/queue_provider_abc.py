import abc


class QueueProvider(abc.ABC):
    @abc.abstractmethod
    def get_waiting_queue(self, aisle_id):
        pass

    @abc.abstractmethod
    def get_active_pool(self, aisle_id):
        pass
