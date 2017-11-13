from symbol import Symbol


class TableSymbol:

    def __init__(self):
        self.stack = [{}]

    def startBlock(self):
        self.stack.append({})

    def endBlock(self):
        if len(self.stack) == 1:
            raise Exception("Canno't close global block")
        self.stack.pop()

    def newSymbol(self, node):
        node_name = node.identifier
        current_block = self._getCurrentBlock()
        if node_name not in current_block:
            symbol = Symbol(node_name, node)
            current_block[node_name] = symbol
            return symbol
        else:
            raise Exception("Canno't declare %s" % (node_name))

    def getSymbol(self, node):
        index = len(self.stack) - 1

        node_name = node.identifier

        while index > 0:
            block = self.stack[index]

            if node_name in block:
                return block[node_name]

            index -= 1

        raise Exception("Undifined symbol %s " % (node_name))


    def _getCurrentBlock(self):
        size = len(self.stack)
        return self.stack[size - 1]