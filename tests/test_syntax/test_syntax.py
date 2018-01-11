import unittest

import syntax
import lexical


class TestSyntax(unittest.TestCase):
    def test_constant(self):
        str = " 3 "
        lex = lexical.Lexical(str)
        syn = syntax.Syntax(lex, run=False)
        node = syn.P(lex.current())

        self.assertEqual(syntax.nodes_const.NODE_CONSTANT, node.type)
        self.assertEqual(3, node.value)

    def test_variable(self):
        str = "x;"
        lex = lexical.Lexical(str)
        syn = syntax.Syntax(lex, run=False)
        node = syn.P(lex.current())

        self.assertEqual(syntax.nodes_const.NODE_VAR_REF, node.type)
        self.assertEqual("x", node.identifier)

    def test_unitary_minus_const(self):
        str = "-4"
        lex = lexical.Lexical(str)
        syn = syntax.Syntax(lex, run=False)
        node = syn.P(lex.current())

        self.assertEqual(syntax.nodes_const.NODE_UNITARY_MINUS, node.type)
        self.assertEqual(1, len(node.children))

        child = node.children[0]

        self.assertEqual(syntax.nodes_const.NODE_CONSTANT, child.type)
        self.assertEqual(4, child.value)

    def test_unitary_minus_ident(self):
        str = "-y;"
        lex = lexical.Lexical(str)
        syn = syntax.Syntax(lex, run=False)
        node = syn.P(lex.current())

        self.assertEqual(syntax.nodes_const.NODE_UNITARY_MINUS, node.type)
        self.assertEqual(1, len(node.children))

        child = node.children[0]

        self.assertEqual(syntax.nodes_const.NODE_VAR_REF, child.type)
        self.assertEqual('y', child.identifier)

    def test_global(self):
        str = "int main() { 3 + x * 2 * -z; }"
        lex = lexical.Lexical(str)

        # self.assertEqual(8 + 6, len(lex))

        syn = syntax.Syntax(lex)

        self.assertEqual(9 + 1, syn.size)

    def test_not(self):
        str = "int main() { !3; }"
        lex = lexical.Lexical(str)

        # self.assertEqual(8 + 6, len(lex))

        syn = syntax.Syntax(lex)

        self.assertEqual(3 + 1, syn.size)

        str = "int main() { !!3; }"
        lex = lexical.Lexical(str)

        # self.assertEqual(8 + 6, len(lex))

        syn = syntax.Syntax(lex)

        self.assertEqual(4 + 1, syn.size)

        str = "int main() { !(!1 + 2); }"
        lex = lexical.Lexical(str)

        # self.assertEqual(8 + 6, len(lex))

        syn = syntax.Syntax(lex)

        self.assertEqual(6 + 1, syn.size)

    def test_cond(self):

        token_cond = ["&&", "||", "==", "!=", "<", "<=", ">", ">="]

        for tok in token_cond:
            print tok
            str = "int main() { 3 %s 1; }" % tok
            lex = lexical.Lexical(str)

            print(', '.join([t.category.name for t in lex.tokens]))
            self.assertEqual(4 + 6, len(lex))

            syn = syntax.Syntax(lex)

            self.assertEqual(4 + 1, syn.size)

    def test_statement_equals(self):

        str = "int main() { 3 == 1; }"
        lex = lexical.Lexical(str)

        print(', '.join([t.category.name for t in lex.tokens]))
        self.assertEqual(4 + 6, len(lex))

        syn = syntax.Syntax(lex)

        self.assertEqual(4 + 1, syn.size)



    def test_cond_e(self):


            str = "3 == 1;"
            lex = lexical.Lexical(str)

            print(', '.join([t.category.name for t in lex.tokens]))
            self.assertEqual(4, len(lex))

            syn = syntax.Syntax(lex, run=False)
            syn.E(lex.current())

            self.assertEqual(3, syn.size)


    def test_error(self):
        str = "int main() { 3 * (2 + 4) * 1 ( }"
        lex = lexical.Lexical(str)

        self.assertEqual(10 + 6, len(lex))

        with self.assertRaises(syntax.SyntaxError) as e:
            syntax.Syntax(lex)
        print(e.exception)

        str = "int main() { 3 * (2 + 4) * 1 1 }"
        lex = lexical.Lexical(str)

        self.assertEqual(10 + 6, len(lex))

        with self.assertRaises(syntax.SyntaxError) as e:
            syntax.Syntax(lex)
        print(e.exception)

        str = "int main() { 3 * (2 + 4) * 1 * }"
        lex = lexical.Lexical(str)

        self.assertEqual(10 + 6, len(lex))

        with self.assertRaises(syntax.SyntaxError) as e:
            syntax.Syntax(lex)
        print(e.exception)

        str = "int main() { 3 * (2 + 4) * 1 ) }"
        lex = lexical.Lexical(str)

        self.assertEqual(10 + 6, len(lex))

        with self.assertRaises(syntax.SyntaxError) as e:
            syntax.Syntax(lex)
        print(e.exception)

        str = "int main() { 3 * (2 + 4) * 1 - }"
        lex = lexical.Lexical(str)

        self.assertEqual(10 + 6, len(lex))

        with self.assertRaises(syntax.SyntaxError) as e:
            syntax.Syntax(lex)
        print(e.exception)


    def test_block(self):

        str = 'int main() { { 3 + 3; 2 +2; } }'

        lex = lexical.Lexical(str)

        self.assertEqual(10 + 6, len(lex))

        syn = syntax.Syntax(lex)

        self.assertEqual(9 + 1, syn.size)


    def test_if(self):
        str = "int main() { if (3 == 2) { 2 + 1; 4 + 3; } }"


        lex = lexical.Lexical(str)

        self.assertEqual(16 + 6, len(lex))

        syn = syntax.Syntax(lex)

        self.assertEqual(13 + 1, syn.size)

    def test_if_else(self):
        str = "int main() { if (3 == 2) { 2 + 1; 4 + 3; } else { 3 + 5; } }"

        lex = lexical.Lexical(str)

        self.assertEqual(23 + 6, len(lex))

        syn = syntax.Syntax(lex)

        self.assertEqual(18 + 1, syn.size)

    def test_declaration(self):
        str = "int main() { int a; }"

        lex = lexical.Lexical(str)

        self.assertEqual(3 + 6, len(lex))

        syn = syntax.Syntax(lex)

        self.assertEqual(1 + 1, syn.size)


    def test_affectation(self):
        str = "int main() { a = 10 + 2; }"

        lex = lexical.Lexical(str)

        self.assertEqual(6 + 6, len(lex))

        syn = syntax.Syntax(lex)

        self.assertEqual(4 + 1, syn.size)


    def test_if_malformated(self):

        str ="if ( 1 || b { 1 + 2; }"

        lex = lexical.Lexical(str)

        self.assertEqual(11, len(lex))

        with self.assertRaises(syntax.SyntaxError) as e:
            syntax.Syntax(lex)
        print(e.exception)

    def test_out(self):
        str = "int main() { out 2; }"

        lex = lexical.Lexical(str)

        self.assertEqual(3 + 6, len(lex))

        syn = syntax.Syntax(lex)

        self.assertEqual(2 + 1, syn.size)

    def test_out_addition(self):
        str = "int main() { out 2 + 1; }"

        lex = lexical.Lexical(str)

        self.assertEqual(5 + 6, len(lex))

        syn = syntax.Syntax(lex)

        self.assertEqual(4 + 1, syn.size)

    def test_while(self):
        str = "int main() { while(1 + 1) 1 + 3;  }"

        self.generic(str, 10, 10)

        str = "int main() { while(1 + 1){ 1 + 3; } }"
        self.generic(str, 12, 11)

    def generic(self, str, lexSize, synSize):
        lex = lexical.Lexical(str)
        self.assertEqual(lexSize + 6, len(lex))

        syn = syntax.Syntax(lex)
        print(syn.node)
        self.assertEqual(synSize + 1, syn.size)

if __name__ == '__main__':
    unittest.main()
