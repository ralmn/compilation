import unittest

import test_lexical
import test_table_symbol

if __name__ == '__main__':
    suite = unittest.TestSuite()
    result = unittest.TestResult()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(test_lexical.TestTokenizer))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(test_table_symbol.TestTableSymbol))
    runner = unittest.TextTestRunner()
    print(runner.run(suite))
