import syntax
from syntax import nodes_const

class Semantic:

    def __init__(self, tableSymbol):
        self.nbVar = 0
        self.tableSymbol = tableSymbol

    def run(self, node):
        if node.type == syntax.nodes_const.NODE_BLOCK:
            self.tableSymbol.startBlock()
            for child in node.children:
                self.run(child)
            self.tableSymbol.endBlock()

        elif node.type == syntax.nodes_const.NODE_VAR_DECL:
            symbol = self.tableSymbol.newSymbol(node)
            symbol.slot = self.nextNbVar()
            node.slot = symbol.slot

        elif node.type == syntax.nodes_const.NODE_VAR_REF or node.type == syntax.nodes_const.NODE_AFFECTATION:
            symbol = self.tableSymbol.getSymbol(node)
            node.slot = symbol.slot
            for child in node.children:
                self.run(child)

        else:
            for child in node.children:
                self.run(child)

    def semLoop(self, node):
        if node.type == nodes_const.NODE_LOOP:
            return
        if node.type == nodes_const.NODE_CONTINUE or node.type == nodes_const.NODE_BREAK:
            # TODO : Faire une sementique exception
            raise Exception("Sementique exception : %s not in loop" % node.type.name)

        for c in node.children:
            self.semLoop(c)


    def nextNbVar(self):
        val = self.nbVar
        self.nbVar += 1
        return val

