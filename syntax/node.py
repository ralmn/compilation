class Node:

    def __init__(self, type, children=[], identifier=None, value=None):
        self.type = type
        self.children = children
        self.identifier = identifier
        self.value = value

    def gencode(self, gCode):
        gencode = self.type.gencode

        if gencode is not None:
            gencode(gCode, self)
        else:
            raise Exception("Umanaged node type.")





