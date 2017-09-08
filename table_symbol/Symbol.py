class Symbol:
    def __init__(self, name, token):
        self.name = name
        self.token = token

    def __eq__(self, other):
        if not (self.__class__.__name__ is other.__class__.__name__):
            return False

        return self.name == other.name \
            and self.token == other.token
