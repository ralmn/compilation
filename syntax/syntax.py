# coding=utf-8
from lexical import categories_const
from node import Node
import nodes_const
from syntax_error import SyntaxError


# P = constant | identifiant | ( E ) | - P | !P

# F = P * F | P / F | P % F | P

# T = F + T | F - T | F

# C -> ==, !=, <, <=, >, >=

# L -> &&

# E -> ||

# S -> '{' S* '}'
#	| A ';'
#	| E ';'
#	| 'if' '(' E ')' S (else S )?
#	| 'int' ident ';'

# A <- ident '=' E



class Syntax:
    def __init__(self, lexical, run=True):
        self.size = 0
        self.lexical = lexical
        self.node = None
        if run:
            self.run()

    def run(self):
        self.node = self.S(self.lexical.current())

        if not self.lexical.isEnd():
            raise SyntaxError("Unexpected token %s" % str(self.lexical.nextToken()))

    def P(self, token):
        if token.category == categories_const.TOKEN_VALUE:
            self.size += 1
            return Node(nodes_const.NODE_CONSTANT, value=token.value)
        if token.category == categories_const.TOKEN_IDENT:
            self.size += 1
            return Node(nodes_const.NODE_IDENTIFIANT, identifier=token.identifier)

        if token.category == categories_const.TOKEN_PARENTHESIS_OPEN:
            node = self.E(self.lexical.nextToken())
            if self.lexical.nextToken().category == categories_const.TOKEN_PARENTHESIS_CLOSE:
                return node

        if token.category == categories_const.TOKEN_MINUS:
            node = self.P(self.lexical.nextToken())

            if node is None:
                raise SyntaxError('NEGATIVE : 2nd part missing, (token: %s)' % str(token))

            self.size += 1
            return Node(nodes_const.NODE_UNITARY_MINUS, [node])

        if token.category == categories_const.TOKEN_NOT:
            node = self.P(self.lexical.nextToken())

            if node is None:
                raise SyntaxError('NOT : 2nd part missing, (token: %s)' % str(token))

            self.size += 1
            return Node(nodes_const.NODE_NOT, [node])
        return None

    def F(self, token):
        node1 = self.P(token)

        if node1 is None:
            return None

        token = self.lexical.nextToken()

        if token is None:
            return node1

        tokensToCheck = {
            categories_const.TOKEN_MULTIPLICATION: nodes_const.NODE_MULT,
            categories_const.TOKEN_DIVIDER: nodes_const.NODE_DIV,
            categories_const.TOKEN_MODULO: nodes_const.NODE_MOD
        }

        if token.category in tokensToCheck:
            nodeType = tokensToCheck[token.category]
            next_token = self.lexical.nextToken()

            if next_token is None:
                raise SyntaxError('%s : 2nd part missing, (token: %s)' % (nodeType.name, str(token)))

            node2 = self.F(next_token)

            if node2 is None:
                raise SyntaxError(
                    '%s : wrong 2nd part, (token: %s, next_token: %s)' % (nodeType.name, str(token), str(next_token)))

            self.size += 1
            return Node(nodeType, [node1, node2])

        self.lexical.undo()
        return node1

    def T(self, token):

        node1 = self.F(token)

        if node1 is None:
            return None

        token = self.lexical.nextToken()

        if token is None:
            return node1

        tokensToCheck = {
            categories_const.TOKEN_PLUS: nodes_const.NODE_ADD,
            categories_const.TOKEN_MINUS: nodes_const.NODE_BINARAY_MINUS,
        }

        if token.category in tokensToCheck:
            nodeType = tokensToCheck[token.category]
            next_token = self.lexical.nextToken()

            if next_token is None:
                raise SyntaxError('%s : 2nd part missing, (token: %s)' % (nodeType.name, str(token)))

            node2 = self.T(next_token)

            if node2 is None:
                raise SyntaxError(
                    '%s : wrong 2nd part, (token: %s, next_token: %s)' % (nodeType.name, str(token), str(next_token)))

            self.size += 1
            return Node(nodeType, [node1, node2])

        self.lexical.undo()
        return node1

    def C(self, token):

        node1 = self.T(token)

        if node1 is None:
            return None

        token = self.lexical.nextToken()

        if token is None:
            return node1

        tokensToCheck = {
            categories_const.TOKEN_EQUALS: nodes_const.NODE_EQUALS,
            categories_const.TOKEN_NOT_EQUALS: nodes_const.NODE_NOT_EQUALS,
            categories_const.TOKEN_LOWER_THAN: nodes_const.NODE_LOWER_THAN,
            categories_const.TOKEN_LOWER_EQUALS_THAN: nodes_const.NODE_LOWER_EQUALS,
            categories_const.TOKEN_GREATER_THAN: nodes_const.NODE_GREATER_THAN,
            categories_const.TOKEN_GREATER_EQUALS_THAN: nodes_const.NODE_GREATER_EQUALS,

        }

        if token.category in tokensToCheck:
            nodeType = tokensToCheck[token.category]
            next_token = self.lexical.nextToken()

            if next_token is None:
                raise SyntaxError('%s : 2nd part missing, (token: %s)' % (nodeType.name, str(token)))

            node2 = self.C(next_token)

            if node2 is None:
                raise SyntaxError(
                    '%s : wrong 2nd part, (token: %s, next_token: %s)' % (nodeType.name, str(token), str(next_token)))

            self.size += 1
            return Node(nodeType, [node1, node2])

        self.lexical.undo()
        return node1

    def L(self, token):

        node1 = self.C(token)

        if node1 is None:
            return None

        token = self.lexical.nextToken()

        if token is None:
            return node1

        tokensToCheck = {
            categories_const.TOKEN_AND: nodes_const.NODE_AND,

        }

        if token.category in tokensToCheck:
            nodeType = tokensToCheck[token.category]
            next_token = self.lexical.nextToken()

            if next_token is None:
                raise SyntaxError('%s : 2nd part missing, (token: %s)' % (nodeType.name, str(token)))

            node2 = self.L(next_token)

            if node2 is None:
                raise SyntaxError('%s : wrong 2nd part, (token: %s, next_token: %s)' % (
                    nodeType.name, str(token), str(next_token)))

            self.size += 1
            return Node(nodeType, [node1, node2])

        self.lexical.undo()
        return node1

    def E(self, token):

        node1 = self.L(token)

        if node1 is None:
            return None

        token = self.lexical.nextToken()

        if token is None:
            return node1

        tokensToCheck = {
            categories_const.TOKEN_OR: nodes_const.NODE_OR,

        }

        if token.category in tokensToCheck:
            nodeType = tokensToCheck[token.category]
            next_token = self.lexical.nextToken()

            if next_token is None:
                raise SyntaxError('%s : 2nd part missing, (token: %s)' % (nodeType.name, str(token)))

            node2 = self.E(next_token)

            if node2 is None:
                raise SyntaxError('%s : wrong 2nd part, (token: %s, next_token: %s)' % (
                    nodeType.name, str(token), str(next_token)))

            self.size += 1
            return Node(nodeType, [node1, node2])

        self.lexical.undo()
        return node1

    def S(self, token):

        nextToken = self.lexical.nextToken()

        if token.category == categories_const.TOKEN_CURLY_BRACKET_OPEN:
            # '{' S* '}'

            nodesBlockChildren = []

            while nextToken is not None and nextToken.category is not categories_const.TOKEN_CURLY_BRACKET_CLOSE:
                nodeS = self.S(nextToken)

                if nodeS is not None:
                    nodesBlockChildren.append(nodeS)
                    nextToken = self.lexical.nextToken()

            if nextToken is None:
                raise SyntaxError('Block : Bracket not closed.(%s) ' % str(token))

            nodeBlock = Node(nodes_const.NODE_BLOCK, nodesBlockChildren)
            nextToken = self.lexical.nextToken()
            return nodeBlock

        # Debut gestion A

        if nextToken is None:
            raise SyntaxError('Statement is not finish (%s)' % str(token))

        nodeA = self.A(token)

        if nodeA is not None:
            nextTokenAfterA = self.lexical.nextToken()

            if nextTokenAfterA.category == categories_const.TOKEN_SEMICOLON:
                return nodeA

            raise SyntaxError("Affectation: Missing semicolon (%s) " % str(token))

        # Fin gestion A

        #Debut gestion E

        nodeE = self.E(token)

        if nodeE is not None:
            nextTokenAfterE = self.lexical.nextToken()

            if nextTokenAfterE.category == categories_const.TOKEN_SEMICOLON:
                return nodeE

            raise SyntaxError("Expression: Missing semicolon (%s) " % str(token))

        # fin gestion E

        # Debut gestion if

        if token.category == categories_const.TOKEN_IF:
            if nextToken.category != categories_const.TOKEN_PARENTHESIS_OPEN:
                raise SyntaxError('IF : Missing opening parenthesis for condition (%s)' % str(token))

            self.lexical.undo()

            nodeCondition = self.E(nextToken)

            if nodeCondition is None:
                raise SyntaxError('IF : Missing condition (%s) ' % str(token))

            nextToken = self.lexical.nextToken()

            if nextToken is None:
                raise SyntaxError('IF : Missing statement (%s) ' % str(token))

            nodeS1 = self.S(nextToken)
            if nodeS1 is None:
                raise SyntaxError('IF : Missing statement (%s) ' % str(token))

            tokenElse = self.lexical.nextToken()
            if tokenElse is None or tokenElse.category != categories_const.TOKEN_ELSE:
                self.lexical.undo()
                return Node(nodes_const.NODE_IF, [nodeCondition, nodeS1])

            nextToken = self.lexical.nextToken()
            nodeS2 = self.S(nextToken)
            if nodeS2 is None:
                raise SyntaxError('Else : Missing statement (%s) ' % str(token))

            return Node(nodes_const.NODE_IF, [nodeCondition, nodeS1, nodeS2])

        # fin gestion IF

        # debut gestion declaration

        if token.category == categories_const.TOKEN_INT:
            if nextToken.category != categories_const.TOKEN_IDENT:
                raise SyntaxError('DECLARATION : Missing identifier (%s)' % str(token))

            nextTokenAfterIdent = self.lexical.nextToken()

            if nextTokenAfterIdent.category == categories_const.TOKEN_SEMICOLON:
                return Node(nodes_const.NODE_VAR_DECL, children=[], identifier=nextToken.identifier)
            else:
                raise SyntaxError('DECLARATION : Missing semicolon (%s)' % str(token))

        # fin gestion declaration

    def A(self, token):

        tokenIden = token

        tokenEquals = self.lexical.nextToken()

        if tokenEquals.category != categories_const.TOKEN_EQUALS:
            self.lexical.undo()
            return None

        tokenExpression = self.lexical.nextToken()

        if tokenExpression is None:
            raise SyntaxError("Affectation : Missing expression after equals (%s) " % str(token))

        nodeAfterExpression = self.E(tokenExpression)

        if nodeAfterExpression is None:
            raise SyntaxError("Affectation : incorrect expression after equals (%s) " % str(token))

        return Node(nodes_const.NODE_AFFECTATION, [nodeAfterExpression], identifier=tokenIden.identifier)