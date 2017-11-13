class Symbol:
    def __init__(self, name, node):
        self.name = name
        self.node = node
        self.slot = None

    def __eq__(self, other):
        if not (self.__class__.__name__ is other.__class__.__name__):
            return False

        return self.name == other.name \
            and self.node == other.node
