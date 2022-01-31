class ActivePool:
    def __init__(self):
        self.elements = []

    def add(self, element):
        self.elements.append(element)

    def remove(self, element):
        self.elements.remove(element)

    def __len__(self):
        return len(self.elements)

    def __contains__(self, element):
        return element in self.elements
