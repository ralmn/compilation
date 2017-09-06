import unittest

import lexical

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(lexical.TestTokenizer("test_tokenizer"))
    unittest.TextTestRunner.run(suite)