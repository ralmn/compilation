import syntax
from syntax import nodes_const

class Semantic:

    def __init__(self, tableSymbol):
        self.nbVar = 0
        self.tableSymbol = tableSymbol

    def run(self, node):
        self.semFunction(node)

    def analyseSemntique(self, node):
        self.semSymbol(node)
        self.semLoop(node)

    def semSymbol(self, node):
        if node.type == syntax.nodes_const.NODE_BLOCK:
            self.tableSymbol.startBlock()
            for child in node.children:
                self.semSymbol(child)
            self.tableSymbol.endBlock()

        elif node.type == syntax.nodes_const.NODE_VAR_DECL:
            symbol = self.tableSymbol.newSymbol(node)
            symbol.slot = self.nextNbVar()
            node.slot = symbol.slot

        elif node.type in [syntax.nodes_const.NODE_VAR_REF, syntax.nodes_const.NODE_AFFECTATION,
                           syntax.nodes_const.NODE_INDIRECTION, syntax.nodes_const.NODE_INDEX]:
            symbol = self.tableSymbol.getSymbol(node)  # TODO : Try except de gestion d'erreur
            node.slot = symbol.slot
            for child in node.children:
                self.semSymbol(child)

        else:
            for child in node.children:
                self.semSymbol(child)

    def semLoop(self, node):
        if node.type == nodes_const.NODE_LOOP:
            return
        if node.type == nodes_const.NODE_CONTINUE or node.type == nodes_const.NODE_BREAK:
            # TODO : Faire une sementique exception
            raise Exception("Sementique exception : %s not in loop" % node.type.name)

        for c in node.children:
            self.semLoop(c)

    def semFunction(self, node):
        if node.type == nodes_const.NODE_PROGRAM:
            for func in node.children:
                self.semFunction(func)
            return
        if node.type == nodes_const.NODE_FUNC:
            self.tableSymbol.newSymbol(node)  # evite 2 fonction du meme nom
            self.nbVar = 0
            self.tableSymbol.startBlock()

            for param in node.params:
                symbolParam = self.tableSymbol.newSymbolIdent(param, node=None)
                symbolParam.slot = self.nextNbVar()

            self.analyseSemntique(node.children[0])

            self.tableSymbol.endBlock()
            node.nbLocal = self.nbVar - len(node.params)

            return

        # TODO : Faire une sementique exception
        raise Exception("Sementique exception : need to define function ")




    def nextNbVar(self):
        val = self.nbVar
        self.nbVar += 1
        return val

