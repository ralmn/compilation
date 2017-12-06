import unittest

import test_lexical
import test_table_symbol
import test_syntax
import tests_run

if __name__ == '__main__':
    suite = unittest.TestSuite()
    result = unittest.TestResult()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(test_lexical.TestTokenizer))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(test_lexical.TestLexical))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(test_table_symbol.TestTableSymbol))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(test_syntax.TestSyntax))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(tests_run.TestRun))
    runner = unittest.TextTestRunner()
    print(runner.run(suite))
