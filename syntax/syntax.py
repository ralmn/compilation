from lexical import categories_const
from node import Node
import nodes_const


class Syntax:

    def __init__(self, lexical):
        self.size = 0
        self.lexical = lexical
        self.node = None

    def run(self):
        self.node = self.T(self.lexical.current())

    def P(self, token):
        if token.category == categories_const.TOKEN_VALUE:
            self.size += 1
            return Node(nodes_const.NODE_CONSTANT, value=token.value)
        if token.category == categories_const.TOKEN_IDENT:
            self.size += 1
            return Node(nodes_const.NODE_IDENTIFIANT, identifier=token.identifier)

        if token.category == categories_const.TOKEN_MINUS:
            node = self.P(self.lexical.nextToken())

            if node is None:
                print('NEGATIVE : 2nd part missing, (token: %s)' % str(token))
                return None

            self.size += 1
            return Node(nodes_const.NODE_UNITARY_MINUS, [node])

        if token.category == categories_const.TOKEN_PARENTHESIS_OPEN:
            node = self.T(self.lexical.nextToken())
            if self.lexical.nextToken().category == categories_const.TOKEN_PARENTHESIS_CLOSE:
                return node

        return None

    def F(self, token):
        node1 = self.P(token)

        if node1 is None:
            return None

        token = self.lexical.nextToken()

        if token is None:
            return node1

        if token.category == categories_const.TOKEN_MULTIPLICATION:
            node2 = self.F(self.lexical.nextToken())

            if node2 is None:
                print('MULT : 2nd part missing, (token: %s)' % str(token))
                return None

            self.size += 1
            return Node(nodes_const.NODE_MULT, [node1, node2])
        elif token.category == categories_const.TOKEN_DIVIDER:
            node2 = self.F(self.lexical.nextToken())

            if node2 is None:
                print('DIV : 2nd part missing, (token: %s)' % str(token))
                return None

            self.size += 1
            return Node(nodes_const.NODE_DIV, [node1, node2])

        self.lexical.undo()
        return node1

    def T(self, token):

        node1 = self.F(token)

        if node1 is None:
            return None

        token = self.lexical.nextToken()

        if token is None:
            return node1

        if token.category == categories_const.TOKEN_PLUS:
            node2 = self.T(self.lexical.nextToken())

            if node2 is None:
                print('ADD : 2nd part missing, (token: %s)' % str(token))
                return None

            self.size += 1
            return Node(nodes_const.NODE_ADD, [node1, node2])
        elif token.category == categories_const.TOKEN_MINUS:
            node2 = self.T(self.lexical.nextToken())

            if node2 is None:
                print('SUB : 2nd part missing, (token: %s)' % str(token))
                return None

            self.size += 1
            return Node(nodes_const.NODE_BINARAY_MINUS, [node1, node2])

        self.lexical.undo()
        return node1





