class NodeType:

    def __init__(self, name, gencode = None):
        self.name = name
        self.gencode = gencode


    def __eq__(self, other):
        if not (self.__class__.__name__ is other.__class__.__name__):
            return False

        return self.name == other.name

    def __repr__(self):
        return "NodeType(%s)" % self.name