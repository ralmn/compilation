from nodes_types import NodeType


def genCodeConst(genCode, node):
    genCode.linesOut.append("push.i %s" % node.value)


def genCodeMath(genCode, command, node):
    node.children[0].gencode(genCode)
    node.children[1].gencode(genCode)
    genCode.linesOut.append(command)

def genCodeUnitaryMinus(genCode, node):
    genCode.linesOut.append("push.i 0")
    node.children[0].gencode(genCode)
    genCode.linesOut.append("sub.i")



NODE_CONSTANT = NodeType("constant", genCodeConst)
NODE_IDENTIFIANT = NodeType("identifiant")

NODE_ADD = NodeType("addition", lambda g, n: genCodeMath(g, "add.i", n) )

NODE_MULT = NodeType("multiplication", lambda g, n: genCodeMath(g, "mul.i", n))
NODE_DIV = NodeType("division", lambda g, n: genCodeMath(g, "div.i", n))

NODE_MOD = NodeType("modulo", lambda g, n: genCodeMath(g, "mod.i", n))

NODE_BINARAY_MINUS = NodeType("binary minus (x - y, substraction)", lambda g, n: genCodeMath(g, "sub.i", n))
NODE_UNITARY_MINUS = NodeType("unitary minus (-x)", genCodeUnitaryMinus)

NODE_NOT = NodeType("not")

NODE_EQUALS = NodeType("equals")
NODE_NOT_EQUALS = NodeType("not equals")
NODE_GREATER_THAN = NodeType("greater than")
NODE_GREATER_EQUALS = NodeType("greater equals")
NODE_LOWER_THAN = NodeType("lower than")
NODE_LOWER_EQUALS = NodeType("lower equals")

NODE_AND = NodeType("and")
NODE_OR = NodeType("or")