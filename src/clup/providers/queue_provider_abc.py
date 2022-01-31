import abc


class QueueProvider(abc.ABC):
    @abc.abstractmethod
    def get_waiting_queue(self, store_id):
        pass

    @abc.abstractmethod
    def get_active_pool(self, store_id):
        pass