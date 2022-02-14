class StorePool:
    def __init__(self):
        self.enabled = []
        self.to_free = []

    def add(self, element):
        self.enabled.append(element)

    def consume(self, element):
        self.enabled.remove(element)
        self.to_free.append(element)

    def free(self, element):
        self.to_free.remove(element)

    def get_to_free(self):
        return self.to_free[:]
