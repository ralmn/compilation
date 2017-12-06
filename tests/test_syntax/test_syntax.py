import unittest

import syntax
import lexical


class TestSyntax(unittest.TestCase):
    def test_constant(self):
        str = "3"
        lex = lexical.Lexical(str)
        syn = syntax.Syntax(lex, run=False)
        node = syn.P(lex.current())

        self.assertEqual(syntax.nodes_const.NODE_CONSTANT, node.type)
        self.assertEqual(3, node.value)

    def test_variable(self):
        str = "x"
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
        str = "-y"
        lex = lexical.Lexical(str)
        syn = syntax.Syntax(lex, run=False)
        node = syn.P(lex.current())

        self.assertEqual(syntax.nodes_const.NODE_UNITARY_MINUS, node.type)
        self.assertEqual(1, len(node.children))

        child = node.children[0]

        self.assertEqual(syntax.nodes_const.NODE_VAR_REF, child.type)
        self.assertEqual('y', child.identifier)

    def test_global(self):
        str = "3 + x * 2 * -z;"
        lex = lexical.Lexical(str)

        # self.assertEqual(8, len(lex))

        syn = syntax.Syntax(lex)

        self.assertEqual(9, syn.size)

    def test_not(self):
        str = "!3;"
        lex = lexical.Lexical(str)

        # self.assertEqual(8, len(lex))

        syn = syntax.Syntax(lex)

        self.assertEqual(3, syn.size)

        str = "!!3;"
        lex = lexical.Lexical(str)

        # self.assertEqual(8, len(lex))

        syn = syntax.Syntax(lex)

        self.assertEqual(4, syn.size)

        str = "!(!1 + 2);"
        lex = lexical.Lexical(str)

        # self.assertEqual(8, len(lex))

        syn = syntax.Syntax(lex)

        self.assertEqual(6, syn.size)

    def test_cond(self):

        token_cond = ["&&", "||", "==", "!=", "<", "<=", ">", ">="]

        for tok in token_cond:
            print tok
            str = "3 %s 1;" % tok
            lex = lexical.Lexical(str)

            print(', '.join([t.category.name for t in lex.tokens]))
            self.assertEqual(4, len(lex))

            syn = syntax.Syntax(lex)

            self.assertEqual(4, syn.size)

    def test_statement_equals(self):

        str = "3 == 1;"
        lex = lexical.Lexical(str)

        print(', '.join([t.category.name for t in lex.tokens]))
        self.assertEqual(4, len(lex))

        syn = syntax.Syntax(lex)

        self.assertEqual(4, syn.size)


    def test_cond_e(self):


            str = "3 == 1"
            lex = lexical.Lexical(str)

            print(', '.join([t.category.name for t in lex.tokens]))
            self.assertEqual(3, len(lex))

            syn = syntax.Syntax(lex, run=False)
            syn.E(lex.current())

            self.assertEqual(3, syn.size)


    def test_error(self):
        str = "3 * (2 + 4) * 1 ("
        lex = lexical.Lexical(str)

        self.assertEqual(10, len(lex))

        with self.assertRaises(syntax.SyntaxError) as e:
            syntax.Syntax(lex)
        print(e.exception)

        str = "3 * (2 + 4) * 1 1"
        lex = lexical.Lexical(str)

        self.assertEqual(10, len(lex))

        with self.assertRaises(syntax.SyntaxError) as e:
            syntax.Syntax(lex)
        print(e.exception)

        str = "3 * (2 + 4) * 1 *"
        lex = lexical.Lexical(str)

        self.assertEqual(10, len(lex))

        with self.assertRaises(syntax.SyntaxError) as e:
            syntax.Syntax(lex)
        print(e.exception)

        str = "3 * (2 + 4) * 1 )"
        lex = lexical.Lexical(str)

        self.assertEqual(10, len(lex))

        with self.assertRaises(syntax.SyntaxError) as e:
            syntax.Syntax(lex)
        print(e.exception)

        str = "3 * (2 + 4) * 1 -"
        lex = lexical.Lexical(str)

        self.assertEqual(10, len(lex))

        with self.assertRaises(syntax.SyntaxError) as e:
            syntax.Syntax(lex)
        print(e.exception)


    def test_block(self):

        str = '{ 3 + 3; 2 +2; }'

        lex = lexical.Lexical(str)

        self.assertEqual(10, len(lex))

        syn = syntax.Syntax(lex)

        self.assertEqual(9, syn.size)


    def test_if(self):
        str = "if (3 == 2) { 2 + 1; 4 + 3; }"


        lex = lexical.Lexical(str)

        self.assertEqual(16, len(lex))

        syn = syntax.Syntax(lex)

        self.assertEqual(13, syn.size)

    def test_if_else(self):
        str = "if (3 == 2) { 2 + 1; 4 + 3; } else { 3 + 5; }"

        lex = lexical.Lexical(str)

        self.assertEqual(23, len(lex))

        syn = syntax.Syntax(lex)

        self.assertEqual(18, syn.size)

    def test_declaration(self):
        str = "int a;"

        lex = lexical.Lexical(str)

        self.assertEqual(3, len(lex))

        syn = syntax.Syntax(lex)

        self.assertEqual(1, syn.size)


    def test_affectation(self):
        str = "a = 10 + 2;"

        lex = lexical.Lexical(str)

        self.assertEqual(6, len(lex))

        syn = syntax.Syntax(lex)

        self.assertEqual(4, syn.size)


    def test_if_malformated(self):

        str ="if ( 1 || b { 1 + 2; }"

        lex = lexical.Lexical(str)

        self.assertEqual(11, len(lex))

        with self.assertRaises(syntax.SyntaxError) as e:
            syntax.Syntax(lex)
        print(e.exception)

    def test_out(self):
        str = "out 2;"

        lex = lexical.Lexical(str)

        self.assertEqual(3, len(lex))

        syn = syntax.Syntax(lex)

        self.assertEqual(2, syn.size)

    def test_out_addition(self):
        str = "out 2 + 1;"

        lex = lexical.Lexical(str)

        self.assertEqual(5, len(lex))

        syn = syntax.Syntax(lex)

        self.assertEqual(4, syn.size)

    def test_while(self):
        str = "while(1 + 1) 1 + 3; "

        self.generic(str, 10, 10)

        str = "while(1 + 1){ 1 + 3; }"
        self.generic(str, 12, 11)

    def generic(self, str, lexSize, synSize):
        lex = lexical.Lexical(str)
        self.assertEqual(lexSize, len(lex))

        syn = syntax.Syntax(lex)
        print(syn.node)
        self.assertEqual(synSize, syn.size)

if __name__ == '__main__':
    unittest.main()
