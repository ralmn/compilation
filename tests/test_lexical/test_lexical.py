import unittest

import lexical


class TestLexical(unittest.TestCase):

    def test_all(self):
        str = "2 + z * 4"
        lex = lexical.Lexical(str)
        self.assertEqual(5, len(lex))

        c = lex.current()
        self.assertEqual(lexical.categories_const.TOKEN_VALUE, c.category)
        self.assertEqual(2, c.value)


        c = lex.nextToken()
        plus = c
        self.assertEqual(lexical.categories_const.TOKEN_PLUS, c.category)

        c = lex.nextToken()
        self.assertEqual(lexical.categories_const.TOKEN_IDENT, c.category)
        self.assertEqual("z", c.identifier)

        c = lex.nextToken()
        self.assertEqual(lexical.categories_const.TOKEN_MULTIPLICATION, c.category)

        c = lex.undo()

        self.assertEqual(lexical.categories_const.TOKEN_IDENT, c.category)
        self.assertEqual("z", c.identifier)

        c = lex.nextToken()
        self.assertEqual(lexical.categories_const.TOKEN_MULTIPLICATION, c.category)

        c = lex.undo(plus)
        self.assertEqual(lexical.categories_const.TOKEN_PLUS, c.category)











if __name__ == '__main__':
    unittest.main()

