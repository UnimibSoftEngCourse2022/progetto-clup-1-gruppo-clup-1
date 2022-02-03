from src.clup.entities.exceptions import EmptyQueueError


class WaitingQueue:
    def __init__(self):
        self.queue = []

    def push(self, element):
        self.queue.insert(0, element)

    def pop(self):
        if len(self) <= 0:
            raise EmptyQueueError()

        return self.queue.pop()

    def insert(self, index, element):
        if index > len(self.queue):
            index = len(self.queue)
        self.queue.insert(len(self.queue) - index, element)

    def remove(self, element):
        if len(self) <= 0:
            raise EmptyQueueError()

        self.queue.remove(element)

    def __len__(self):
        return len(self.queue)

    def __contains__(self, element):
        return element in self.queue

    def __iter__(self):
        return iter(self.queue)
