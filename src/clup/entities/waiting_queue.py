class WaitingQueue:
    def __init__(self):
        self.queue = []

    def push(self, element):
        self.queue.insert(0, element)

    def pop(self):
        return self.queue.pop()

    def insert(self, index, element):
        if index > len(self.queue):
            index = len(self.queue)
        self.queue.insert(len(self.queue) - index, element)

    def __len__(self):
        return len(self.queue)

    def __contains__(self, element):
        return element in self.queue
