import unittest

import test_lexical
import test_table_symbol
import test_syntax

if __name__ == '__main__':
    suite = unittest.TestSuite()
    result = unittest.TestResult()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(test_lexical.TestTokenizer))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(test_lexical.TestLexical))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(test_table_symbol.TestTableSymbol))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(test_syntax.TestSyntax))
    runner = unittest.TextTestRunner()
    print(runner.run(suite))
