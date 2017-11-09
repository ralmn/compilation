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
        self.assertEqual([lexical.Token(lexical.categories_const.TOKEN_VALUE, 1, 1, value=2489)], tokens)

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

    def test_fullIf(self):
        tokens = lexical.tokenizer.tokenize("if(int a, int b){ \r\n}")

        # print('\n'.join([str(t) for t in tokens]))

        self.assertEqual(10, len(tokens))

        self.assertEqual(1, tokens[0].column)
        self.assertEqual(3, tokens[1].column)
        self.assertEqual(4, tokens[2].column)
        self.assertEqual(8, tokens[3].column)
        self.assertEqual(9, tokens[4].column)
        self.assertEqual(11, tokens[5].column)
        self.assertEqual(15, tokens[6].column)
        self.assertEqual(16, tokens[7].column)
        self.assertEqual(17, tokens[8].column)
        self.assertEqual(1, tokens[9].column)
        self.assertEqual(2, tokens[9].line)


    def test_and(self):
        tokens = lexical.tokenizer.tokenize("1 && 2")
        self.assertEqual(3, len(tokens))
        self.assertEqual("value", tokens[0].category.name)
        self.assertEqual("and", tokens[1].category.name)
        self.assertEqual("value", tokens[2].category.name)

    def test_or(self):
        tokens = lexical.tokenizer.tokenize("1 || 2")
        self.assertEqual(3, len(tokens))
        self.assertEqual("value", tokens[0].category.name)
        self.assertEqual("or", tokens[1].category.name)
        self.assertEqual("value", tokens[2].category.name)

    def test_lower(self):
        tokens = lexical.tokenizer.tokenize("1 < 2")
        self.assertEqual(3, len(tokens))
        self.assertEqual("value", tokens[0].category.name)
        self.assertEqual("lower than", tokens[1].category.name)
        self.assertEqual("value", tokens[2].category.name)

    def test_lower_equals(self):
        tokens = lexical.tokenizer.tokenize("1 <= 2")
        self.assertEqual(3, len(tokens))
        self.assertEqual("value", tokens[0].category.name)
        self.assertEqual("lower equals than", tokens[1].category.name)
        self.assertEqual("value", tokens[2].category.name)



if __name__ == '__main__':
    unittest.main()

