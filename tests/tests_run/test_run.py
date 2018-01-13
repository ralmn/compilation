from __future__ import print_function
from subprocess import check_output


import unittest
import os, io, subprocess

import sys

import signal

import main
import syntax
from compile_exception import CompileException


class TestRun(unittest.TestCase):


    def test_compile_perso(self):

        dir_path = os.path.dirname(os.path.realpath(__file__))
        for dirname, dirnames, filenames in os.walk(os.path.join(dir_path, '../../tests_perso/pass')):
            for file in filenames:
                if '.txt' in file or '.cmm' in file:
                    p = os.path.join(dirname, file)
                    self.runFile(p)

    def test_exec_perso(self):

        dir_path = os.path.dirname(os.path.realpath(__file__))
        for dirname, dirnames, filenames in os.walk(os.path.join(dir_path, '../../tests_perso/pass')):

            for file in filenames:
                if '.txt' in file or '.cmm' in file:
                    p = os.path.join(dirname, file)
                    pathOut = os.path.join(dirname, file.replace('.txt', '.out').replace('.cmm', '.out'))

                    file = open(pathOut, 'r')
                    lines = file.readlines()

                    process = subprocess.Popen(os.path.join(dir_path, '../../MSM/msm'),
                                           stdin=subprocess.PIPE, stdout=subprocess.PIPE)

                    self.runFile(p, out=process.stdin, skip_print=False)


                    process.stdin.close()
                    rc = process.wait()
                    #print('rc', rc)

                    assert rc == 0

                    linesOut = []

                    for line in process.stdout:
                        linesOut.append(line)

                    print('lines', lines, linesOut)
                    assert ''.join(lines) == ''.join(linesOut)


    def test_compile_prof(self):

        dir_path = os.path.dirname(os.path.realpath(__file__))
        for dirname, dirnames, filenames in os.walk(os.path.join(dir_path, '../../tests_prof/pass')):
            for file in filenames:
                if '.txt' in file or '.cmm' in file:
                    p = os.path.join(dirname, file)
                    self.runFile(p, appendMain=True)

    def test_exec_prof(self):

        dir_path = os.path.dirname(os.path.realpath(__file__))
        for dirname, dirnames, filenames in os.walk(os.path.join(dir_path, '../../tests_prof/pass')):

            for file in filenames:
                if '.txt' in file or '.cmm' in file:
                    p = os.path.join(dirname, file)
                    pathOut = os.path.join(dirname, file.replace('.txt', '.out'))
                    file = open(pathOut, 'r')
                    lines = file.readlines()

                    process = subprocess.Popen(os.path.join(dir_path, '../../MSM/msm'),
                                           stdin=subprocess.PIPE, stdout=subprocess.PIPE)

                    self.runFile(p, out=process.stdin, skip_print=False, appendMain=True)


                    process.stdin.close()
                    rc = process.wait()
                    #print('rc', rc)

                    assert rc == 0

                    linesOut = []

                    for line in process.stdout:
                        linesOut.append(line)

                    print('lines', lines, linesOut)
                    assert ''.join(lines) == ''.join(linesOut)


    @unittest.skip("test de debug")
    def test_specifique(self):
        file = 'pass.033.txt'
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dirname = os.path.join(dir_path, '../../tests_prof/pass')
        p = os.path.join(dirname, file)
        self.runFile(p, skip_print=False)

    def runFile(self, path, skip_print=True, out=sys.stdout, appendMain=False):
        print('Run file %s ' % path)

        try:
            file = open(path, 'r')
            lines = file.readlines()
            if appendMain:
                lines.insert(0, 'int main()')
            #lines.append('}')
            main.run('\n'.join(lines), skip_print=skip_print, out=out)

        except IOError as e:
            print('\n'.join(lines))
            print("File error :", e, file=sys.stderr)

        except CompileException as e:
            print('\n'.join(lines))
            print(e.message, file=sys.stderr)
            raise e


if __name__ == '__main__':
    unittest.main()
