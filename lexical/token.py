class Token:

    def __init__(self, category, line, column, identifier = None, value = None):
        self.line = line
        self.category = category

