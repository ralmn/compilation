import unittest

import lexical


class TestTokenizer(unittest.TestCase):

    def test_identifiant(self):
        tokens = lexical.tokenizer.tokenize("slt")
        self.assertEqual(1, len(tokens))
        self.assertEqual([lexical.Token(lexical.categories_const.TOKEN_IDENT, 1, 1, identifier="slt")], tokens)

    def test_value(self):
        tokens = lexical.tokenizer.tokenize("2489")
        self.assertEqual(1, len(tokens))
        self.assertEqual([lexical.Token(lexical.categories_const.TOKEN_VALUE, 1, 1, value="2489")], tokens)

    def test_if(self):
        tokens = lexical.tokenizer.tokenize("if")
        self.assertEqual(1, len(tokens))
        self.assertEqual([lexical.Token(lexical.categories_const.TOKEN_IF, 1, 1)], tokens)

    def test_parenthesis(self):
        tokens = lexical.tokenizer.tokenize("(")
        self.assertEqual(1, len(tokens))
        self.assertEqual([lexical.Token(lexical.categories_const.TOKEN_PARENTHESIS_OPEN, 1, 1)], tokens)

        tokens = lexical.tokenizer.tokenize(")")
        self.assertEqual(1, len(tokens))
        self.assertEqual([lexical.Token(lexical.categories_const.TOKEN_PARENTHESIS_CLOSE, 1, 1)], tokens)



if __name__ == '__main__':
    unittest.main()

