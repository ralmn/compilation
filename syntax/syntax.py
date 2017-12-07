# coding=utf-8
from lexical import categories_const
from node import Node
import nodes_const
from syntax_error import SyntaxError


# P = constant | ident ('[' E ']')? | identifiant '(' [ [E,]* E]?  ')' | ( E ) | - P | !P | * ident

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
#   | break | continue | return | while | do while | for

# A <- ident ('[' E ']')? '=' E | * ident  '=' E

# D -> int ident '(' [int ident]* ')' S

# Z -> D*

class Syntax:
    def __init__(self, lexical, run=True):
        self.size = 0
        self.lexical = lexical
        self.node = None
        if run:
            self.run()

    def run(self):  # Z
        # self.node = self.S(self.lexical.current())
        # if self.node is None:
        #     raise SyntaxError("Unexpected statement %s" % str(self.lexical.tokens[0]))
        # self.lexical.nextToken()
        # if not self.lexical.isEnd():
        #     raise SyntaxError("Unexpected token %s" % str(self.lexical.nextToken()))

        childrenNodeProg = []

        while not self.lexical.isEnd():
            node = self.D(self.lexical.current())
            childrenNodeProg.append(node)
            self.lexical.nextToken()

        self.node = Node(type=nodes_const.NODE_PROGRAM, children=childrenNodeProg)

    def P(self, token):
        if token.category == categories_const.TOKEN_VALUE:
            self.size += 1
            return Node(nodes_const.NODE_CONSTANT, value=token.value)

        if token.category == categories_const.TOKEN_IDENT:
            self.size += 1

            next_token = self.lexical.nextToken()
            if next_token is None:
                raise SyntaxError('Identifier with nothing after, (token: %s)' % (str(token)))

            if next_token.category == categories_const.TOKEN_PARENTHESIS_OPEN:
                list_param = []

                while not self.lexical.isEnd():
                    next_token = self.lexical.nextToken()
                    if next_token is None:
                        raise SyntaxError('function called but argument are not finished, (token: %s)' % (str(token)))
                    if next_token.category == categories_const.TOKEN_PARENTHESIS_CLOSE:
                        self.size += 1
                        return Node(nodes_const.NODE_FUNC_CALL, identifier=token.identifier, children=list_param)

                    next_node = self.P(next_token)
                    if next_node is None:
                        raise SyntaxError('Function called but parametter is not valid, (token: %s)' % (str(next_token)))

                    list_param.append(next_node)

                    # we don't return => return None at end of function

            else:
                self.lexical.undo()
                return Node(nodes_const.NODE_VAR_REF, identifier=token.identifier)

        if token.category == categories_const.TOKEN_PARENTHESIS_OPEN:
            node = self.E(self.lexical.nextToken())
            nxtToken = self.lexical.nextToken()
            if nxtToken.category == categories_const.TOKEN_PARENTHESIS_CLOSE:
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

        if token.category == categories_const.TOKEN_CURLY_BRACKET_OPEN:
            # '{' S* '}'
            nextToken = self.lexical.nextToken()

            nodesBlockChildren = []

            while nextToken is not None and nextToken.category is not categories_const.TOKEN_CURLY_BRACKET_CLOSE:
                nodeS = self.S(nextToken)

                if nodeS is not None:
                    nodesBlockChildren.append(nodeS)
                    nextToken = self.lexical.nextToken()

            if nextToken is None:
                raise SyntaxError('Block : Bracket not closed.(%s) ' % str(token))

            nodeBlock = Node(nodes_const.NODE_BLOCK, nodesBlockChildren)
            #nextToken = self.lexical.nextToken()
            self.size += 1
            return nodeBlock

        # Debut gestion A

        # if nextToken is None:
        #     raise SyntaxError('Statement is not finish (%s)' % str(token))

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
                self.size += 1
                return Node(nodes_const.NODE_DROP, [nodeE])

            raise SyntaxError("Expression: Missing semicolon (%s) " % str(token))

        # fin gestion E

        # debut gestion out

        if token.category == categories_const.TOKEN_OUT:
            nextToken = self.lexical.nextToken()

            if nextToken is None:
                raise SyntaxError("Out: Missing expression to print (%s)" % str(token))

            nodeExpression = self.E(nextToken)

            if nodeExpression is None:
                raise SyntaxError("Out: unexpected expression to print (%s)" % str(nextToken))

            nextTokenAfterE = self.lexical.nextToken()

            if nextTokenAfterE.category == categories_const.TOKEN_SEMICOLON:
                self.size += 1
                return Node(nodes_const.NODE_OUT, [nodeExpression])

            raise SyntaxError("Out: Missing semicolon (%s) " % str(token))


        # fin gestion out

        # Debut gestion if

        if token.category == categories_const.TOKEN_IF:

            nextToken = self.lexical.nextToken()

            if nextToken is None:
                raise SyntaxError('IF : not finished statement (%s)' % str(token))

            if nextToken.category != categories_const.TOKEN_PARENTHESIS_OPEN:
                raise SyntaxError('IF : Missing opening parenthesis for condition (%s)' % str(token))

            #self.lexical.undo()

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
                #self.lexical.undo()
                self.size += 1
                return Node(nodes_const.NODE_IF, [nodeCondition, nodeS1])

            nextToken = self.lexical.nextToken()
            nodeS2 = self.S(nextToken)
            if nodeS2 is None:
                raise SyntaxError('Else : Missing statement (%s) ' % str(token))
            self.size += 1
            return Node(nodes_const.NODE_IF, [nodeCondition, nodeS1, nodeS2])

        # fin gestion IF


        # debut gestion WHILE

        if token.category == categories_const.TOKEN_WHILE:
            nextToken = self.lexical.nextToken()

            if nextToken is None:
                raise SyntaxError('WHILE : not finished statement (%s)' % str(token))

            if nextToken.category != categories_const.TOKEN_PARENTHESIS_OPEN:
                raise SyntaxError('WHILE : Missing opening parenthesis for condition (%s)' % str(token))

            # self.lexical.undo()

            nodeCondition = self.E(nextToken)

            if nodeCondition is None:
                raise SyntaxError('WHILE : Missing condition (%s) ' % str(token))

            nextToken = self.lexical.nextToken()

            if nextToken is None:
                raise SyntaxError('WHILE : Missing statement (%s) ' % str(token))

            nodeS = self.S(nextToken)
            if nodeS is None:
                raise SyntaxError('WHILE : Missing statement (%s) ' % str(token))

            self.size += 3 # loop + if + ?????BREAK POURQUOI ON LA PAS ?
            nodeIf = Node(nodes_const.NODE_IF, children=[nodeCondition, nodeS, Node(nodes_const.NODE_BREAK)])
            arrayIf = []
            arrayIf.append(nodeIf)


            return Node(nodes_const.NODE_LOOP, children=[nodeIf])

        # fin gestion WHILE

        #debut gestion break

        if token.category == categories_const.TOKEN_BREAK:
            self.size += 1
            nextToken = self.lexical.nextToken()
            return Node(nodes_const.NODE_BREAK)

        #fin gestion break

        # debut gestion continue

        if token.category == categories_const.TOKEN_CONTINUE:
            self.size += 1
            nextToken = self.lexical.nextToken()
            return Node(nodes_const.NODE_CONTINUE)

        # fin gestion continue

        # debut gestion return

        if token.category == categories_const.TOKEN_RETURN:

            nextToken = self.lexical.nextToken()
            if nextToken is None:
                raise SyntaxError("return: Missing return value (%s)" % token)

            children = []

            # With return value
            if nextToken.category != categories_const.TOKEN_SEMICOLON:
                nodeE = self.E(nextToken)
                if nodeE is None:
                    raise SyntaxError("return: Invalid return value (%s) " % token)
                children.append(nodeE)
                nextToken = self.lexical.nextToken()

            if nextToken.category != categories_const.TOKEN_SEMICOLON:
                raise SyntaxError("return: Missing semicolon (%s)" % token)

            self.size += 1
            return Node(nodes_const.NODE_RETURN, children=children)

        # fin gestion return

        # debut gestion declaration

        if token.category == categories_const.TOKEN_INT:

            nextToken = self.lexical.nextToken()

            if nextToken is None:
                raise SyntaxError('DECLARATION : incomplete statement (%s)' % str(token))

            if nextToken.category != categories_const.TOKEN_IDENT:
                raise SyntaxError('DECLARATION : Missing identifier (%s)' % str(token))

            nextTokenAfterIdent = self.lexical.nextToken()

            if nextTokenAfterIdent.category == categories_const.TOKEN_SEMICOLON:
                self.size += 1
                return Node(nodes_const.NODE_VAR_DECL, children=[], identifier=nextToken.identifier)
            else:
                raise SyntaxError('DECLARATION : Missing semicolon (%s)' % str(token))

        # fin gestion declaration

    def A(self, token):

        tokenIden = token

        tokenEquals = self.lexical.nextToken()

        if tokenEquals.category != categories_const.TOKEN_AFFECT:
            self.lexical.undo()
            return None

        tokenExpression = self.lexical.nextToken()

        if tokenExpression is None:
            raise SyntaxError("Affectation : Missing expression after equals (%s) " % str(token))

        nodeAfterExpression = self.E(tokenExpression)

        if nodeAfterExpression is None:
            raise SyntaxError("Affectation : incorrect expression after equals (%s) " % str(token))

        self.size += 1
        return Node(nodes_const.NODE_AFFECTATION, [nodeAfterExpression], identifier=tokenIden.identifier)

    def D(self, token):
        if token.category != categories_const.TOKEN_INT:
            raise SyntaxError("Function : Missing int (%s) " % str(token))

        nextTokenIdent = self.lexical.nextToken()
        if nextTokenIdent.category != categories_const.TOKEN_IDENT:
            raise SyntaxError("Function : Missing function name (%s) " % str(nextTokenIdent))

        nextToken = self.lexical.nextToken()
        if nextToken.category != categories_const.TOKEN_PARENTHESIS_OPEN:
            raise SyntaxError("Function : Missing opening parenthesis (%s) " % str(nextToken))

        nextToken = self.lexical.nextToken()

        params = []

        while nextToken.category == categories_const.TOKEN_INT:
            nextToken = self.lexical.nextToken()
            if nextToken.category != categories_const.TOKEN_IDENT:
                raise SyntaxError("Function : Missing params name (%s) " % str(nextToken))
            params.append(nextToken.identifier)

            nextToken = self.lexical.nextToken()
            if nextToken.category != categories_const.TOKEN_COMMA:
                #nextToken = self.lexical.nextToken()
                break

            nextToken = self.lexical.nextToken()


        if nextToken.category != categories_const.TOKEN_PARENTHESIS_CLOSE:
            raise SyntaxError("Function : Missing closing parenthesis (%s) " % str(nextToken))

        nextToken = self.lexical.nextToken()

        nodeS = self.S(nextToken)
        if nodeS is None:
            raise SyntaxError("Function : Missing function body (%s) " % str(nextToken))

        return Node(type=nodes_const.NODE_FUNC, children=[nodeS], params=params, identifier=nextTokenIdent.identifier)





