import unittest
import table_symbol
from lexical import Token, categories_const

class TestTableSymbol(unittest.TestCase):

    def test_openBlock(self):
        table = table_symbol.TableSymbol()
        self.assertEqual(1, len(table.stack))
        table.startBlock()
        self.assertEqual(2, len(table.stack))
        table.startBlock()
        self.assertEqual(3, len(table.stack))

    def test_closeBlock(self):
        table = table_symbol.TableSymbol()
        table.startBlock()
        table.startBlock()
        self.assertEqual(3, len(table.stack))
        table.endBlock()
        self.assertEqual(2, len(table.stack))
        table.endBlock()
        self.assertEqual(1, len(table.stack))

        with self.assertRaises(Exception):
            table.endBlock()

    def test_createSymbol(self):
        table = table_symbol.TableSymbol()
        table.startBlock()

        token_foo = Token(categories_const.TOKEN_IDENT, 1, 1, identifier="foo")
        token_foo2 = Token(categories_const.TOKEN_IDENT, 2, 1, identifier="foo")
        token_bar = Token(categories_const.TOKEN_IDENT, 1, 1, identifier="bar")

        symbol = table.newSymbol(token_foo)

        self.assertEqual(table_symbol.Symbol(token_foo.identifier, token_foo), symbol)

        symbol_bar = table.newSymbol(token_bar)
        self.assertEqual(table_symbol.Symbol(token_bar.identifier, token_bar), symbol_bar)

        with self.assertRaises(Exception):
            symbol_foo = table.newSymbol(token_foo)

        table.startBlock()
        symbol_foo2 = table.newSymbol(token_foo2)
        self.assertEqual(table_symbol.Symbol(token_foo2.identifier, token_foo2), symbol_foo2)

    def test_getSymbol(self):
        table = table_symbol.TableSymbol()
        table.startBlock()

        token_foo = Token(categories_const.TOKEN_IDENT, 1, 1, identifier="foo")
        token_bar = Token(categories_const.TOKEN_IDENT, 1, 1, identifier="bar")
        token_albert = Token(categories_const.TOKEN_IDENT, 1, 1, identifier="albert")

        token_foo2 = Token(categories_const.TOKEN_IDENT, 2, 1, identifier="foo")

        symbol = table.newSymbol(token_foo)
        symbol_bar = table.newSymbol(token_bar)

        self.assertEqual(symbol, table.getSymbol(token_foo))
        self.assertEqual(symbol_bar, table.getSymbol(token_bar))

        with self.assertRaises(Exception):
            table.getSymbol(token_albert)

        table.startBlock()

        self.assertEqual(symbol, table.getSymbol(token_foo))
        self.assertEqual(symbol_bar, table.getSymbol(token_bar))

        with self.assertRaises(Exception):
            table.getSymbol(token_albert)

        symbol_foo2 = table.newSymbol(token_foo2)
        self.assertEqual(symbol_foo2, table.getSymbol(token_foo2))







if __name__ == '__main__':
    unittest.main()

