class Category:

    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

    def __eq__(self, other):
        if not (self.__class__.__name__ is other.__class__.__name__):
            return False

        return self.symbol == other.symbol

    def __repr__(self):
        return "Category(%s)" % self.name



