from src.clup.entities.subject_abc import Subject


class StorePool(Subject):
    def __init__(self):
        self.enabled = []
        self.to_free = []
        self.last_added = None
        self._observers = []

    def add(self, element):
        self.enabled.append(element)
        self.last_added = element
        self.notify()

    def consume(self, element):
        self.enabled.remove(element)
        self.to_free.append(element)

    def free(self, element):
        self.to_free.remove(element)

    def get_to_free(self):
        return self.to_free[:]

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self)
