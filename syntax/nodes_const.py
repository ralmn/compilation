from nodes_types import NodeType


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
    pass


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

NODE_VAR_DECL = NodeType("Variable declaration")
NODE_VAR_REF = NodeType("Variable reference")
NODE_AFFECTATION = NodeType("Affectation")

NODE_IF = NodeType("if")