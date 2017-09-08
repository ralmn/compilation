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

    def newSymbol(self, token):
        token_name = token.identifier
        current_block = self._getCurrentBlock()
        if token_name not in current_block:
            symbol = Symbol(token_name, token)
            current_block[token_name] = symbol
            return symbol
        else:
            raise Exception("Canno't declare %s (line: %d, column %d)" % (token_name, token.line, token.column))

    def getSymbol(self, token):
        index = len(self.stack) - 1

        token_name = token.identifier

        while index > 0:
            block = self.stack[index]

            if token_name in block:
                return block[token_name]

            index -= 1

        raise Exception("Undifined symbol %s (line: %d, column %d)" % (token_name, token.line, token.column))


    def _getCurrentBlock(self):
        size = len(self.stack)
        return self.stack[size - 1]