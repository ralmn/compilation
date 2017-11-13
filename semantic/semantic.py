import syntax

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
            symbol = self.tableSymbol.newSymbol(node.token)
            symbol.slot = self.nextNbVar()

        elif node.type == syntax.nodes_const.NODE_VAR_REF or node.type == syntax.nodes_const.NODE_AFFECTATION:
            symbol = self.tableSymbol.getSymbol(node)
            node.slot = symbol.slot
        else:
            for child in node.children:
                self.run(child)


    def nextNbVar(self):
        self.nbVar += 1
        return self.nbVar

