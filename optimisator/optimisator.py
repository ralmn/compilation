import syntax

class Optimisator:

    def __init__(self, node):
        self.node = node
        self.run()

    def run(self):
        self.opti_minus_sub(self.node)
        self.node = self.opt_minus(self.node)
        self.node = self.opt_operation(self.node)
        # TODO : optimisation condition logique


    def opti_minus_sub(self, node):
        """
        Optimisation du
            "- (a - b)" ==> "-a + b"
            "- (a + b)  ==> "-a -b"
        On fait le changement a la volee
        :param node:
        :return:
        """
        if node.type == syntax.nodes_const.NODE_UNITARY_MINUS:
            child = node.children[0]
            if child.type == syntax.nodes_const.NODE_BINARAY_MINUS:
                node.type = syntax.nodes_const.NODE_ADD
                node.children[0] = syntax.Node(syntax.nodes_const.NODE_UNITARY_MINUS, [child.children[0]])
                node.children.append(child.children[1])
            elif child.type == syntax.nodes_const.NODE_ADD:
                node.type = syntax.nodes_const.NODE_BINARAY_MINUS
                node.children[0] = syntax.Node(syntax.nodes_const.NODE_UNITARY_MINUS, [child.children[0]])
                node.children.append(child.children[1])

        for i in range(len(node.children)):
            self.opti_minus_sub(node.children[i])

    def opt_minus(self, node):
        for i in range(len(node.children)):
            node.children[i] = self.opt_minus(node.children[i])
        if node.type == syntax.nodes_const.NODE_UNITARY_MINUS:
            res = node.children[0]
            if res.type == syntax.nodes_const.NODE_CONSTANT:
                res.value = - res.value
                return res
        return node

    def opt_operation(self, node):
        for i in range(len(node.children)):
            node.children[i] = self.opt_operation(node.children[i])
        if node.type == syntax.nodes_const.NODE_BINARAY_MINUS \
                and node.children[0].type == syntax.nodes_const.NODE_CONSTANT \
                and node.children[1].type == syntax.nodes_const.NODE_CONSTANT:
            return syntax.Node(syntax.nodes_const.NODE_CONSTANT, value=node.children[0].value-node.children[1].value)
        if node.type == syntax.nodes_const.NODE_ADD \
                and node.children[0].type == syntax.nodes_const.NODE_CONSTANT \
                and node.children[1].type == syntax.nodes_const.NODE_CONSTANT:
            return syntax.Node(syntax.nodes_const.NODE_CONSTANT, value=node.children[0].value+node.children[1].value)
        if node.type == syntax.nodes_const.NODE_MULT \
                and node.children[0].type == syntax.nodes_const.NODE_CONSTANT \
                and node.children[1].type == syntax.nodes_const.NODE_CONSTANT:
            return syntax.Node(syntax.nodes_const.NODE_CONSTANT, value=node.children[0].value*node.children[1].value)
        if node.type == syntax.nodes_const.NODE_DIV \
                and node.children[0].type == syntax.nodes_const.NODE_CONSTANT \
                and node.children[1].type == syntax.nodes_const.NODE_CONSTANT:
            return syntax.Node(syntax.nodes_const.NODE_CONSTANT, value=node.children[0].value/node.children[1].value)
        return node
