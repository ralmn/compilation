from __future__ import print_function

import sys
import lexical, syntax, gencode, optimisator


def run(str):

    lex = lexical.Lexical(str)

    node = syntax.Syntax(lex).node

    # TODO : Semantique

    node_opti = optimisator.Optimisator(node).node
    g = gencode.CodeGenerator(node_opti)
    print(g.getOutput())



if __name__ == '__main__':
    try:
        if len(sys.argv) >= 2:
            file = open(sys.argv[1], 'r')
            lines = file.readlines()

            run('\n'.join(lines))
        else:
            run('\n'.join(sys.stdin))
    except IOError as e:
        print("File error :", e, file=sys.stderr)
    except syntax.SyntaxError as e:
        print(e.message, file=sys.stderr)


