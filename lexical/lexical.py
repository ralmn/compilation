class Lexical:
    def __init__(self, tokens=[]):
        self.tokens = tokens
        self.index = 0

    def current(self):
        return self.tokens[self.index]

    def next(self):
        self.index += 1
        return self.current()

    def undo(self, token_to_go=None):
        if token_to_go is not None:
            self.index = self.tokens.index(token_to_go)
        else:
            self.index -= 1
        return self.current()
