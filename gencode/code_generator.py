class CodeGenerator:

    def __init__(self, node):
        self.node = node
        self.linesOut = []
        self.run()


    def run(self):
        self.linesOut.append(".start")

        self.node.gencode(self)

        self.linesOut.append("out.i")
        self.linesOut.append("halt")

    def getOutput(self):
        return '\n'.join(self.linesOut)


