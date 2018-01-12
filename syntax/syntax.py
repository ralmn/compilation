# coding=utf-8
from lexical import categories_const
from node import Node
import nodes_const
from compile_error import CompileError


# import pydot


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
        #     raise CompileError("Unexpected statement %s" % str(self.lexical.tokens[0]))
        # self.lexical.nextToken()
        # if not self.lexical.isEnd():
        #     raise CompileError("Unexpected token %s" % str(self.lexical.nextToken()))

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
                raise CompileError('Identifier with nothing after, (token: %s)' % (str(token)))

            if next_token.category == categories_const.TOKEN_SQUARE_BRACKET_OPEN:
                next_token = self.lexical.nextToken()

                nodeE = self.E(next_token)

                if nodeE is None:
                    raise CompileError("Index read : Invalid expression (%s)" % token)

                next_token = self.lexical.nextToken()
                if next_token.category != categories_const.TOKEN_SQUARE_BRACKET_CLOSE:
                    raise CompileError("Index read : Missing closing bracket (%s)" % token)

                self.size += 1
                return Node(nodes_const.NODE_INDEX, [nodeE], identifier=token.identifier)


            if next_token.category == categories_const.TOKEN_PARENTHESIS_OPEN:
                list_param = []

                while not self.lexical.isEnd():
                    next_token = self.lexical.nextToken()
                    if next_token is None:
                        raise CompileError('function called but argument are not finished, (token: %s)' % (str(token)))
                    if next_token.category == categories_const.TOKEN_PARENTHESIS_CLOSE:
                        self.size += 1
                        return Node(nodes_const.NODE_FUNC_CALL, identifier=token.identifier, children=list_param)

                    next_node = self.E(next_token)
                    if next_node is None:
                        raise CompileError('Function called but parametter is not valid, (token: %s)' % (str(next_token)))

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
                raise CompileError('NEGATIVE : 2nd part missing, (token: %s)' % str(token))

            self.size += 1
            return Node(nodes_const.NODE_UNITARY_MINUS, [node])

        if token.category == categories_const.TOKEN_NOT:
            node = self.P(self.lexical.nextToken())

            if node is None:
                raise CompileError('NOT : 2nd part missing, (token: %s)' % str(token))

            self.size += 1
            return Node(nodes_const.NODE_NOT, [node])

        if token.category == categories_const.TOKEN_MULTIPLICATION:
            node = self.P(self.lexical.nextToken())

            if node is None:
                raise CompileError('NOT : 2nd part missing, (token: %s)' % str(token))

            self.size += 1
            return Node(nodes_const.NODE_INDIRECTION, [], identifier=node.identifier)



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
                raise CompileError('%s : 2nd part missing, (token: %s)' % (nodeType.name, str(token)))

            node2 = self.F(next_token)

            if node2 is None:
                raise CompileError(
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
                raise CompileError('%s : 2nd part missing, (token: %s)' % (nodeType.name, str(token)))

            node2 = self.T(next_token)

            if node2 is None:
                raise CompileError(
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
                raise CompileError('%s : 2nd part missing, (token: %s)' % (nodeType.name, str(token)))

            node2 = self.C(next_token)

            if node2 is None:
                raise CompileError(
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
                raise CompileError('%s : 2nd part missing, (token: %s)' % (nodeType.name, str(token)))

            node2 = self.L(next_token)

            if node2 is None:
                raise CompileError('%s : wrong 2nd part, (token: %s, next_token: %s)' % (
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
                raise CompileError('%s : 2nd part missing, (token: %s)' % (nodeType.name, str(token)))

            node2 = self.E(next_token)

            if node2 is None:
                raise CompileError('%s : wrong 2nd part, (token: %s, next_token: %s)' % (
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
                raise CompileError('Block : Bracket not closed.(%s) ' % str(token))

            nodeBlock = Node(nodes_const.NODE_BLOCK, nodesBlockChildren)
            #nextToken = self.lexical.nextToken()
            self.size += 1
            return nodeBlock

        # Debut gestion A

        # if nextToken is None:
        #     raise CompileError('Statement is not finish (%s)' % str(token))

        nodeA = self.A(token)

        if nodeA is not None:
            nextTokenAfterA = self.lexical.nextToken()

            if nextTokenAfterA.category == categories_const.TOKEN_SEMICOLON:
                return nodeA

            raise CompileError("Affectation: Missing semicolon (%s) " % str(token))

        # Fin gestion A

        #Debut gestion E

        nodeE = self.E(token)

        if nodeE is not None:
            nextTokenAfterE = self.lexical.nextToken()

            if nextTokenAfterE.category == categories_const.TOKEN_SEMICOLON:
                self.size += 1
                return Node(nodes_const.NODE_DROP, [nodeE])

            raise CompileError("Expression: Missing semicolon (%s) " % str(token), token)

        # fin gestion E

        # debut gestion out

        if token.category == categories_const.TOKEN_OUT:
            nextToken = self.lexical.nextToken()

            if nextToken is None:
                raise CompileError("Out: Missing expression to print (%s)" % str(token))

            nodeExpression = self.E(nextToken)

            if nodeExpression is None:
                raise CompileError("Out: unexpected expression to print (%s)" % str(nextToken))

            nextTokenAfterE = self.lexical.nextToken()

            if nextTokenAfterE.category == categories_const.TOKEN_SEMICOLON:
                self.size += 1
                return Node(nodes_const.NODE_OUT, [nodeExpression])

            raise CompileError("Out: Missing semicolon (%s) " % str(token))


        # fin gestion out

        # Debut gestion if

        if token.category == categories_const.TOKEN_IF:

            nextToken = self.lexical.nextToken()

            if nextToken is None:
                raise CompileError('IF : not finished statement (%s)' % str(token))

            if nextToken.category != categories_const.TOKEN_PARENTHESIS_OPEN:
                raise CompileError('IF : Missing opening parenthesis for condition (%s)' % str(token))

            #self.lexical.undo()

            nodeCondition = self.E(nextToken)

            if nodeCondition is None:
                raise CompileError('IF : Missing condition (%s) ' % str(token))

            nextToken = self.lexical.nextToken()

            if nextToken is None:
                raise CompileError('IF : Missing statement (%s) ' % str(token))

            nodeS1 = self.S(nextToken)
            if nodeS1 is None:
                raise CompileError('IF : Missing statement (%s) ' % str(token))

            tokenElse = self.lexical.nextToken()
            if tokenElse is None or tokenElse.category != categories_const.TOKEN_ELSE:
                self.lexical.undo()
                self.size += 1
                return Node(nodes_const.NODE_IF, [nodeCondition, nodeS1])

            nextToken = self.lexical.nextToken()
            nodeS2 = self.S(nextToken)
            if nodeS2 is None:
                raise CompileError('Else : Missing statement (%s) ' % str(token))
            self.size += 1
            return Node(nodes_const.NODE_IF, [nodeCondition, nodeS1, nodeS2])

        # fin gestion IF


        # debut gestion WHILE

        if token.category == categories_const.TOKEN_WHILE:
            nextToken = self.lexical.nextToken()

            if nextToken is None:
                raise CompileError('WHILE : not finished statement (%s)' % str(token))

            if nextToken.category != categories_const.TOKEN_PARENTHESIS_OPEN:
                raise CompileError('WHILE : Missing opening parenthesis for condition (%s)' % str(token))

            # self.lexical.undo()

            nodeCondition = self.E(nextToken)

            if nodeCondition is None:
                raise CompileError('WHILE : Missing condition (%s) ' % str(token))

            nextToken = self.lexical.nextToken()

            if nextToken is None:
                raise CompileError('WHILE : Missing statement (%s) ' % str(token))

            nodeS = self.S(nextToken)
            if nodeS is None:
                raise CompileError('WHILE : Missing statement (%s) ' % str(token))

            self.size += 3
            nodeIf = Node(nodes_const.NODE_IF, children=[nodeCondition, nodeS, Node(nodes_const.NODE_BREAK)])
            arrayIf = []
            arrayIf.append(nodeIf)


            return Node(nodes_const.NODE_LOOP, children=[nodeIf])

        # fin gestion WHILE


        # debut gestion DO-WHILE

        if token.category == categories_const.TOKEN_DO:
            nextToken = self.lexical.nextToken()

            if nextToken is None:
                raise CompileError('DO-WHILE : not finished statement (%s)' % str(token))


            nodeS = self.S(nextToken)

            if nodeS is None:
                raise CompileError('DO-WHILE : invalid block (%s)' % str(token))

            nextToken = self.lexical.nextToken()
            if nextToken.category != categories_const.TOKEN_WHILE:
                raise CompileError('DO-WHILE : Missing While (%s)' % str(token))

            nextToken = self.lexical.nextToken()
            if nextToken.category != categories_const.TOKEN_PARENTHESIS_OPEN:
                raise CompileError('DO-WHILE : Missing opening parenthesis for condition (%s)' % str(token))

            # self.lexical.undo()

            nodeCondition = self.E(nextToken)

            if nodeCondition is None:
                raise CompileError('DO-WHILE : Missing condition (%s) ' % str(token))


            self.size += 5
            nodeIf = Node(nodes_const.NODE_IF, children=[nodeCondition, Node(nodes_const.NODE_CONTINUE), Node(nodes_const.NODE_BREAK)])
            arrayIf = []
            arrayIf.append(nodeIf)

            nodeBlock = Node(nodes_const.NODE_BLOCK, children=[nodeS, nodeIf])
            nodeLoop = Node(nodes_const.NODE_LOOP, children=[nodeBlock])
            return nodeLoop

        # fin gestion DO-WHILE

        # debut gestion for

        if token.category == categories_const.TOKEN_FOR:
            nextToken = self.lexical.nextToken()

            if nextToken is None:
                raise CompileError('FOR : not finished statement (%s)' % str(token))

            if nextToken.category != categories_const.TOKEN_PARENTHESIS_OPEN:
                raise CompileError('FOR : Missing opening parenthesis for params (%s)' % str(token))

            # self.lexical.undo()

            # AFFECTATION

            nextToken = self.lexical.nextToken()
            if nextToken is None:
                raise CompileError('FOR : Missing init affectation statement (%s)' % str(token))

            nodeAffectation = self.A(nextToken)
            if nodeAffectation is None:
                raise CompileError('FOR : invalid init affectation statement (%s) ' % str(token))

            # FIN AFFECTATION

            nextToken = self.lexical.nextToken()
            if nextToken is None or nextToken.category != categories_const.TOKEN_SEMICOLON:
                raise CompileError('FOR : Missing semicolon betweet affectation and condition statement (%s)' % str(token))

            # Condition

            nextToken = self.lexical.nextToken()
            if nextToken is None:
                raise CompileError('FOR : Missing init condition statement (%s)' % str(token))

            nodeCondition = self.E(nextToken)
            if nodeCondition is None:
                raise CompileError('FOR : invalid init condition statement (%s) ' % str(token))

            # Fin condtion

            nextToken = self.lexical.nextToken()
            if nextToken is None or nextToken.category != categories_const.TOKEN_SEMICOLON:
                raise CompileError(
                    'FOR : Missing semicolon betweet condition and incrementation statement (%s)' % str(token))

            # Incrementation

            nextToken = self.lexical.nextToken()
            if nextToken is None:
                raise CompileError('FOR : Missing init incrementation statement (%s)' % str(token))

            nodeIncrementation = self.A(nextToken)
            if nodeIncrementation is None:
                raise CompileError('FOR : invalid init incrementation statement (%s) ' % str(token))

            #fin incrementation

            nextToken = self.lexical.nextToken()
            if nextToken is None:
                raise CompileError('FOR : not finished statement (%s)' % str(token))

            if nextToken.category != categories_const.TOKEN_PARENTHESIS_CLOSE:
                raise CompileError('FOR : Missing closing parenthesis for params (%s)' % str(token))

            nextToken = self.lexical.nextToken()

            if nextToken is None:
                raise CompileError('FOR : missing block (%s)' % str(token))
            nodeS = self.S(nextToken)
            if nodeS is None:
                raise CompileError('FOR : invalid block (%s)' % str(token))

            self.size += 4

            #nodeS.children.append(nodeIncrementation)

            nodeIf = Node(nodes_const.NODE_IF, children=[nodeCondition, nodeS, Node(nodes_const.NODE_BREAK)])
            nodeLoop = Node(nodes_const.NODE_LOOP, children=[nodeIncrementation, nodeIf])
            nodeBlock = Node(nodes_const.NODE_BLOCK, children=[nodeAffectation, nodeLoop])

            return nodeBlock

        # fin gestion for

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
                raise CompileError("return: Missing return value (%s)" % token)

            children = []

            # With return value
            if nextToken.category != categories_const.TOKEN_SEMICOLON:
                nodeE = self.E(nextToken)
                if nodeE is None:
                    raise CompileError("return: Invalid return value (%s) " % token)
                children.append(nodeE)
                nextToken = self.lexical.nextToken()

            if nextToken.category != categories_const.TOKEN_SEMICOLON:
                raise CompileError("return: Missing semicolon (%s)" % token)

            self.size += 1
            return Node(nodes_const.NODE_RETURN, children=children)

        # fin gestion return

        # debut gestion declaration

        if token.category == categories_const.TOKEN_INT:

            nextToken = self.lexical.nextToken()

            if nextToken is None:
                raise CompileError('DECLARATION : incomplete statement (%s)' % str(token))
            #
            # if nextToken.category == categories_const.TOKEN_MULTIPLICATION:
            #     nodeP = self.P(nextToken)
            #     return nodeP

            if nextToken.category != categories_const.TOKEN_IDENT:
                raise CompileError('DECLARATION : Missing identifier (%s)' % str(token))

            nextTokenAfterIdent = self.lexical.nextToken()

            if nextTokenAfterIdent.category == categories_const.TOKEN_SEMICOLON:
                self.size += 1
                return Node(nodes_const.NODE_VAR_DECL, children=[], identifier=nextToken.identifier)
            else:
                raise CompileError('DECLARATION : Missing semicolon (%s)' % str(token))

        # fin gestion declaration

    def A(self, token):

        # c'est un pointeur
        if token.category == categories_const.TOKEN_MULTIPLICATION:
            tokenPtn = token
            tokenIdent = self.lexical.nextToken()

            if tokenIdent.category != categories_const.TOKEN_IDENT:
                raise CompileError("Pointeur : missing identifier (%s)" % str(tokenPtn))

            nextToken = self.lexical.nextToken()

            if nextToken.category == categories_const.TOKEN_SEMICOLON:
                self.lexical.undo(tokenPtn)
                return None

            if nextToken.category != categories_const.TOKEN_AFFECT:
                raise CompileError("Pointeur : missing equals (%s)" % str(tokenPtn))

            #nextToken = self.lexical.nextToken()

            nodeE = self.E(self.lexical.nextToken())

            if nodeE is None:
                raise CompileError("Pointeur : Missing expression (%s)" % str(tokenPtn))

            self.size += 1
            return Node(nodes_const.NODE_INDIRECTION, [nodeE], identifier=tokenIdent.identifier)



        tokenIden = token

        nextToken = self.lexical.nextToken()

        # if [ E ] -> index

        if nextToken.category == categories_const.TOKEN_SQUARE_BRACKET_OPEN:
            #on doit etre en index

            nextToken = self.lexical.nextToken()

            nodeE = self.E(nextToken)

            if nodeE is None:
                raise CompileError("Index : Missing expression (%s)" % str(token))

            nextToken = self.lexical.nextToken()
            if nextToken.category != categories_const.TOKEN_SQUARE_BRACKET_CLOSE:
                raise CompileError("Index : Missing closing square bracket (%s)" % str(token))

            nextToken = self.lexical.nextToken()

            if nextToken.category != categories_const.TOKEN_AFFECT:
                raise CompileError("Index : Missing Affectation (%s)" % str(token))

            tokenExpression = self.lexical.nextToken()

            if tokenExpression is None:
                raise CompileError("Index : Missing expression after equals (%s) " % str(token))

            nodeAfterExpression = self.E(tokenExpression)

            if nodeAfterExpression is None:
                raise CompileError("Index : incorrect expression after equals (%s) " % str(token))

            self.size += 1
            return Node(nodes_const.NODE_INDEX, [nodeE, nodeAfterExpression], identifier=tokenIden.identifier)


        if nextToken.category != categories_const.TOKEN_AFFECT:
            self.lexical.undo()
            return None

        tokenExpression = self.lexical.nextToken()

        if tokenExpression is None:
            raise CompileError("Affectation : Missing expression after equals (%s) " % str(token))

        nodeAfterExpression = self.E(tokenExpression)

        if nodeAfterExpression is None:
            raise CompileError("Affectation : incorrect expression after equals (%s) " % str(token))

        self.size += 1
        return Node(nodes_const.NODE_AFFECTATION, [nodeAfterExpression], identifier=tokenIden.identifier)

    def D(self, token):
        if token.category != categories_const.TOKEN_INT:
            raise CompileError("Function : Missing int (%s) " % str(token))

        nextTokenIdent = self.lexical.nextToken()
        if nextTokenIdent.category != categories_const.TOKEN_IDENT:
            raise CompileError("Function : Missing function name (%s) " % str(nextTokenIdent))

        nextToken = self.lexical.nextToken()
        if nextToken.category != categories_const.TOKEN_PARENTHESIS_OPEN:
            raise CompileError("Function : Missing opening parenthesis (%s) " % str(nextToken))

        nextToken = self.lexical.nextToken()

        params = []

        while nextToken.category == categories_const.TOKEN_INT:
            nextToken = self.lexical.nextToken()
            if nextToken.category != categories_const.TOKEN_IDENT:
                raise CompileError("Function : Missing params name (%s) " % str(nextToken))
            params.append(nextToken.identifier)

            nextToken = self.lexical.nextToken()
            if nextToken.category != categories_const.TOKEN_COMMA:
                #nextToken = self.lexical.nextToken()
                break

            nextToken = self.lexical.nextToken()


        if nextToken.category != categories_const.TOKEN_PARENTHESIS_CLOSE:
            raise CompileError("Function : Missing closing parenthesis (%s) " % str(nextToken))

        nextToken = self.lexical.nextToken()

        nodeS = self.S(nextToken)
        if nodeS is None:
            raise CompileError("Function : Missing function body (%s) " % str(nextToken))

        return Node(type=nodes_const.NODE_FUNC, children=[nodeS], params=params, identifier=nextTokenIdent.identifier)



    def draw(self):
        pass


    #def draw(self):
    #    graph = pydot.Dot()
    #    self.draw_node(graph, self.node)
    #    graph.write_png("tree.png") # , prog="./dot/bin/dot"
    #    #os.startfile(os.path.join(os.getcwd(), "tree.png"))


    # @staticmethod
    # def draw_node(graph, node):
    #     node_display = 'None'
    #     if node is not None:
    #         if node.type == nodes_const.NODE_CONSTANT:
    #             node_display = node.value
    #         elif node.type == nodes_const.NODE_PROGRAM:
    #             node_display = "Start"
    #         elif node.type == nodes_const.NODE_VAR_DECL:
    #             node_display = "decl {}".format(node.identifier)
    #         elif node.type == nodes_const.NODE_VAR_REF:
    #             node_display = node.identifier
    #         else:
    #             node_display = node.type.name
    #
    #     pydot_node = pydot.Node("{}".format(hash(node)), label=node_display)
    #     graph.add_node(pydot_node)
    #     if node is None:
    #         return pydot_node
    #     for child in node.children:
    #         pydot_child = Syntax.draw_node(graph, child)
    #         graph.add_edge(pydot.Edge(pydot_node, pydot_child))
    #     return pydot_node
