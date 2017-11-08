class CodeGenerator:

    def __init__(self, syntax):
        self.syntax = syntax
        self.linesOut = []
        self.run()


    def run(self):
        self.linesOut.append(".start")
        node = self.syntax.node

        node.gencode(self)

        self.linesOut.append("out.i")
        self.linesOut.append("halt")

    def getOutput(self):
        return '\n'.join(self.linesOut)


