from __future__ import print_function

import sys
import lexical, syntax, gencode, optimisator, table_symbol, semantic


def run(str, skip_print=False, out=sys.stdout):

    str = runtime() + str

    tableSymbol = table_symbol.TableSymbol()

    lex = lexical.Lexical(str)

    syn = syntax.Syntax(lex)
    node = syn.node

    syn.draw()

    sem = semantic.Semantic(tableSymbol)
    sem.run(node)


    node = optimisator.Optimisator(node).node
    g = gencode.CodeGenerator(node)
    if not skip_print:
        print(g.getOutput(), file=out)


def runtime():
    return """
        int print(int a) {

            if(a < 10) {
                out a+48;
                return;
            }
        
            int tmp;
            tmp = a/10;
            print(tmp);
        
            out a%10+48;
        }
    """

if __name__ == '__main__':
    try:
        if len(sys.argv) >= 2:
            file = open(sys.argv[1], 'r')
            lines = file.readlines()

            run(''.join(lines))
        else:
            run(''.join(sys.stdin))
    except IOError as e:
        print("File error :", e, file=sys.stderr)
    except syntax.SyntaxError as e:
        print(e.message, file=sys.stderr)


