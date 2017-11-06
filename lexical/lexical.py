import tokenizer


class Lexical:
    def __init__(self, input_str):
        self.tokens = tokenizer.tokenize(input_str)
        self.index = 0

    def current(self):
        if self.index >= len(self.tokens):
           return None
        return self.tokens[self.index]

    def nextToken(self):
        self.index += 1
        return self.current()

    def undo(self, token_to_go=None):
        if token_to_go is not None:
            self.index = self.tokens.index(token_to_go)
        else:
            self.index -= 1
        return self.current()

    def __len__(self):
        return len(self.tokens)
