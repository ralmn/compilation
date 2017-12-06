from nodes_types import NodeType


idLabel = 0

labelStack = []
lStart = None
lEnd = None


def genLabel():
    global idLabel
    idLabel += 1
    return "label" + str(idLabel)

def genCodeConst(genCode, node):
    genCode.linesOut.append("push.i %s" % node.value)


def genCodeMathOrConditional(genCode, command, node):
    node.children[0].gencode(genCode)
    node.children[1].gencode(genCode)
    genCode.linesOut.append(command)


def genCodeUnitaryMinus(genCode, node):
    genCode.linesOut.append("push.i 0")
    node.children[0].gencode(genCode)
    genCode.linesOut.append("sub.i")


def genCodeNot(genCode, node):
    node.children[0].gencode(genCode)
    genCode.linesOut.append("not")


def genCodeBlock(genCode, node):
    for c in node.children:
        c.gencode(genCode)


def genCodeOut(genCode, node):
    node.children[0].gencode(genCode)
    genCode.linesOut.append("out.i")


def genCodeDrop(genCode, node):
    node.children[0].gencode(genCode)
    genCode.linesOut.append("drop")


def genCodeIf(genCode, node):
    l_else = genLabel()

    node.children[0].gencode(genCode)
    genCode.linesOut.append("jumpf %s" % l_else)
    node.children[1].gencode(genCode)

    hasElse = len(node.children) == 3
    if hasElse:
        l_after = genLabel()
        genCode.linesOut.append("jump %s" % l_after)

    genCode.linesOut.append(".%s" % l_else)

    if hasElse:
        node.children[2].gencode(genCode)
        genCode.linesOut.append(".%s" % l_after)


def genCodeLoop(genCode, node):

    global lStart, lEnd, labelStack

    labelStack.append(lStart)
    labelStack.append(lEnd)

    lStart = genLabel()
    lEnd = genLabel()

    genCode.linesOut.append("; debut while")
    genCode.linesOut.append(".%s" % lStart)

    nodeIf = node.children[0]

    E = nodeIf.children[0]
    S = nodeIf.children[1]

    E.gencode(genCode)
    genCode.linesOut.append("jumpf %s" % lEnd)

    S.gencode(genCode)
    genCode.linesOut.append("jump %s" % lStart)

    genCode.linesOut.append(".%s" % lEnd)

    genCode.linesOut.append("; fin while")

    lEnd = labelStack.pop()
    lStart = labelStack.pop()


def genCodeBreak(genCode, node):
    global lEnd
    genCode.linesOut.append("jump %s ; break" % lEnd)  # lEnd


def genCodeContinue(genCode, node):
    global lStart
    genCode.linesOut.append("jump %s ; continue" % lStart)  # lStart


def genCodeDecl(genCode, node):
    genCode.linesOut.append("; int %s (decl) (ignoré car géré dans le gencode de fnc)" % node.identifier)
    pass


def genCodeAffectation(genCode, node):
    node.children[0].gencode(genCode)
    genCode.linesOut.append("set %s ; %s (affect) " % (node.slot, node.identifier))


def genCodeRef(genCode, node):
    genCode.linesOut.append("get %s ; %s (ref)" % (node.slot, node.identifier))


def genCodeIndirection(genCode, node):
    genCode.linesOut.append("get %s ; * %s (pointeur)" % (node.slot, node.identifier))
    if len(node.children) == 0: #lecture
        genCode.linesOut.append("read ; * %s (pointeur)" % (node.identifier))
    else:  #ecriture
        node.children[0].gencode(genCode)  # E
        genCode.linesOut.append("write ; * %s = ... (pointeur set)" % (node.identifier))


def genCodeIndex(genCode, node):
    genCode.linesOut.append("get %s ; %s[E] (index)" % (node.slot, node.identifier))
    node.children[0].gencode(genCode)  # E
    genCode.linesOut.append("add.i")
    if len(node.children) == 1:  # lecture
        genCode.linesOut.append("read ; %s[E] (index)" % (node.identifier))
    else:
        node.children[1].gencode(genCode)  # E
        genCode.linesOut.append("write ; %s[E0] = E1 (index set)" % (node.identifier))


def genCodeFunction(genCode, node):
    genCode.linesOut.append("; Start function %s " % node.identifier)

    genCode.linesOut.append(".%s" % node.identifier)

    for i in range(node.nbLocal):
        genCode.linesOut.append("push.i 9999 ; variable local")  # Utile ?

    node.children[0].gencode(genCode)

    genCode.linesOut.append("push.i 0 ; dans le cas ou on a pas de return")
    genCode.linesOut.append("ret")
    genCode.linesOut.append("; fin function %s " % node.identifier)


def genCodeProgram(genCode, node):

    for child in node.children:
        child.gencode(genCode)

    genCode.linesOut.append(".start")
    genCode.linesOut.append("prep main")
    genCode.linesOut.append("call 0")

    genCode.linesOut.append("halt")

NODE_CONSTANT = NodeType("constant", genCodeConst)
NODE_IDENTIFIANT = NodeType("identifiant")

NODE_ADD = NodeType("addition", lambda g, n: genCodeMathOrConditional(g, "add.i", n))

NODE_MULT = NodeType("multiplication", lambda g, n: genCodeMathOrConditional(g, "mul.i", n))
NODE_DIV = NodeType("division", lambda g, n: genCodeMathOrConditional(g, "div.i", n))

NODE_MOD = NodeType("modulo", lambda g, n: genCodeMathOrConditional(g, "mod.i", n))

NODE_BINARAY_MINUS = NodeType("binary minus (x - y, substraction)", lambda g, n: genCodeMathOrConditional(g, "sub.i", n))
NODE_UNITARY_MINUS = NodeType("unitary minus (-x)", genCodeUnitaryMinus)

NODE_NOT = NodeType("not", genCodeNot)

NODE_EQUALS = NodeType("equals", lambda g, n: genCodeMathOrConditional(g, "cmpeq.i", n))
NODE_NOT_EQUALS = NodeType("not equals", lambda g, n: genCodeMathOrConditional(g, "cmpne.i", n))
NODE_GREATER_THAN = NodeType("greater than", lambda g, n: genCodeMathOrConditional(g, "cmpgt.i", n))
NODE_GREATER_EQUALS = NodeType("greater equals", lambda g, n: genCodeMathOrConditional(g, "cmpge.i", n))
NODE_LOWER_THAN = NodeType("lower than", lambda g, n: genCodeMathOrConditional(g, "cmplt.i", n))
NODE_LOWER_EQUALS = NodeType("lower equals", lambda g, n: genCodeMathOrConditional(g, "cmple.i", n))

NODE_AND = NodeType("and", lambda g, n: genCodeMathOrConditional(g, "and", n))
NODE_OR = NodeType("or", lambda g, n: genCodeMathOrConditional(g, "or", n))

NODE_BLOCK = NodeType("block", genCodeBlock)

NODE_VAR_DECL = NodeType("Variable declaration", genCodeDecl)
NODE_VAR_REF = NodeType("Variable reference", genCodeRef)
NODE_AFFECTATION = NodeType("Affectation", genCodeAffectation)

NODE_DROP = NodeType('Drop', genCodeDrop)

NODE_OUT = NodeType("out", genCodeOut)

NODE_IF = NodeType("if", genCodeIf)

NODE_LOOP = NodeType("loop", genCodeLoop)
NODE_BREAK = NodeType("break", genCodeBreak)
NODE_CONTINUE = NodeType("continue", genCodeContinue)


NODE_FUNC = NodeType("function", genCodeFunction)

NODE_INDIRECTION = NodeType("indirection", genCodeIndirection)  # * ident -> (pointeur)
NODE_INDEX = NodeType('index', genCodeIndex)  # ident [ E ]

NODE_PROGRAM = NodeType("program", genCodeProgram)