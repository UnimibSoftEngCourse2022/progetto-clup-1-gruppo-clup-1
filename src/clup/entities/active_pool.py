from src.clup.entities.exceptions import MaxCapacityReachedError


class ActivePool:
    def __init__(self, capacity=0):
        self.elements = []
        self._capacity = capacity

    def add(self, element):
        if self._capacity == len(self):
            raise MaxCapacityReachedError()
        self.elements.append(element)

    def remove(self, element):
        self.elements.remove(element)

    def __len__(self):
        return len(self.elements)

    def __contains__(self, element):
        return element in self.elements

    def get_capacity(self):
        return self._capacity

    def set_capacity(self, value):
        if value < 0:
            raise ValueError('capacity is negative')

        if value < len(self):
            raise ValueError('capacity is less than current size')

        self._capacity = value

    def delete_capacity(self):
        del self._capacity

    capacity = property(get_capacity, set_capacity, delete_capacity)
