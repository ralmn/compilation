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

        self.assertEqual(syntax.nodes_const.NODE_IDENTIFIANT, node.type)
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

        self.assertEqual(syntax.nodes_const.NODE_IDENTIFIANT, child.type)
        self.assertEqual('y', child.identifier)

    def test_global(self):
        str = "3 + x * 2 * -z"
        lex = lexical.Lexical(str)

        # self.assertEqual(8, len(lex))

        syn = syntax.Syntax(lex)

        self.assertEqual(8, syn.size)

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


if __name__ == '__main__':
    unittest.main()
