# coding=utf-8
from lexical import categories_const
from node import Node
import nodes_const
from syntax_error import SyntaxError

# P = constant | identifiant | ( T ) | - P

# F = P * F | P / F | P % F | P

# T = F + T | F - T | F

class Syntax:

    def __init__(self, lexical, run=True):
        self.size = 0
        self.lexical = lexical
        self.node = None
        if run:
            self.run()

    def run(self):
        self.node = self.T(self.lexical.current())

        if not self.lexical.isEnd():
            raise SyntaxError("Unexpected token %s" % str(self.lexical.nextToken()))


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
                raise SyntaxError('NEGATIVE : 2nd part missing, (token: %s)' % str(token))

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
            next_token = self.lexical.nextToken()

            if next_token is None:
                raise SyntaxError('MULT : 2nd part missing, (token: %s)' % str(token))

            node2 = self.F(next_token)

            if node2 is None:
                raise SyntaxError('MULT : wrong 2nd part, (token: %s, next_token: %s)' % (str(token), str(next_token)))

            self.size += 1
            return Node(nodes_const.NODE_MULT, [node1, node2])
        elif token.category == categories_const.TOKEN_DIVIDER:
            next_token = self.lexical.nextToken()

            if next_token is None:
                raise SyntaxError('DIV : 2nd part missing, (token: %s)' % str(token))

            node2 = self.F(next_token)

            if node2 is None:
                raise SyntaxError('DIV : wrong 2nd part, (token: %s, next_token: %s)' % (str(token), str(next_token)))

            self.size += 1
            return Node(nodes_const.NODE_DIV, [node1, node2])

        elif token.category == categories_const.TOKEN_MODULO:
            next_token = self.lexical.nextToken()

            if next_token is None:
                raise SyntaxError('MOD : 2nd part missing, (token: %s)' % str(token))

            node2 = self.F(next_token)

            if node2 is None:
                raise SyntaxError('MOD : wrong 2nd part, (token: %s, next_token: %s)' % (str(token), str(next_token)))

            self.size += 1
            return Node(nodes_const.NODE_MOD, [node1, node2])

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
            next_token = self.lexical.nextToken()

            if next_token is None:
                raise SyntaxError('ADD : 2nd part missing, (token: %s)' % str(token))

            node2 = self.T(next_token)

            if node2 is None:
                raise SyntaxError('ADD : wrong 2nd part, (token: %s, next_token: %s)' % (str(token), str(next_token)))

            self.size += 1
            return Node(nodes_const.NODE_ADD, [node1, node2])
        elif token.category == categories_const.TOKEN_MINUS:
            next_token = self.lexical.nextToken()

            if next_token is None:
                raise SyntaxError('ADD : 2nd part missing, (token: %s)' % str(token))

            node2 = self.T(next_token)

            if node2 is None:
                raise SyntaxError('SUB : wrong 2nd part, (token: %s, next_token: %s)' % (str(token), str(next_token)))

            self.size += 1
            return Node(nodes_const.NODE_BINARAY_MINUS, [node1, node2])

        self.lexical.undo()
        return node1





