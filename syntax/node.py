class Node:

    def __init__(self, type, children=None, identifier=None, value=None, params=None, token=None):
        if children is None:
            children = []
        self.type = type
        self.children = children
        self.identifier = identifier
        self.value = value
        self.params = params
        self.nbLocal = 0
        self.slot = None
        self.token = token

    def gencode(self, gCode):
        gencode = self.type.gencode

        if gencode is not None:
            gencode(gCode, self)
        else:
            raise Exception("Umanaged node type. %s" % self.type)

    def __repr__(self):
        # return "Node (%s, nbChild=%s, ident=%s, val=%s, slot=%s)" % (self.type, len(self.children), self.identifier, self.value, self.slot)

        return "%s(%s)" % (self.type.name, ', '.join([str(c) for c in self.children]))






