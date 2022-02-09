class StoreActivePool:
    def __init__(self):
        self.pool = []
        self.to_free = []

    def add(self, element):
        self.pool.append(element)

    def consume(self, element):
        self.pool.remove(element)
        self.to_free.append(element)

    def free(self, element):
        self.to_free.remove(element)

    def get_to_free(self):
        return self.to_free[:]
