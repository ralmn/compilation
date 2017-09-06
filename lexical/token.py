class Token:
    def __init__(self, category, line, column, identifier=None, value=None):
        self.value = value
        self.identifier = identifier
        self.column = column
        self.line = line
        self.category = category

    def __eq__(self, other):
        if not (self.__class__.__name__ is other.__class__.__name__):
            return False

        return self.category == other.category \
               and self.line == other.line \
               and self.column == other.column \
               and self.identifier == other.identifier \
               and self.value == other.value


    def __repr__(self):
        return "Token(cat=%s, line=%d, column=%d, identifier=%s, value=%s)" % (self.category, self.line, self.column, self.identifier, self.value)