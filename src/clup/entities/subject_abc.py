import abc


class Subject(abc.ABC):
    @abc.abstractmethod
    def attach(self, observer):
        pass

    @abc.abstractmethod
    def detach(self, observer):
        pass

    @abc.abstractmethod
    def notify(self):
        pass
