import abc


class EmailServiceProvider(abc.ABC):
    @abc.abstractmethod
    def send(self, to, msg):
        pass
