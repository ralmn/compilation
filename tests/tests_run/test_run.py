from __future__ import print_function

import unittest
import os

import sys

import signal

import main
import syntax


class TestRun(unittest.TestCase):
    def test_pass(self):

        for dirname, dirnames, filenames in os.walk('../../tests_prog/pass'):
            for file in filenames:
                if '.txt' in file:
                    p = os.path.join(dirname, file)
                    self.runFile(p)

    def runFile(self, path):
        print('Run file %s ' % path)

        try:
            file = open(path, 'r')
            lines = file.readlines()

            main.run('\n'.join(lines), skip_print=True)

        except IOError as e:
            print('\n'.join(lines))

            print("File error :", e, file=sys.stderr)

        except syntax.SyntaxError as e:
            print('\n'.join(lines))
            print(e.message, file=sys.stderr)

    if __name__ == '__main__':
        unittest.main()
