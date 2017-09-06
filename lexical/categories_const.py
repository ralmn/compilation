from category import Category

# Keyword
TOKEN_IF = Category("if", "if")
TOKEN_ELSE = Category("else", "else")
TOKEN_FOR = Category("for", "for")
TOKEN_DO = Category("do", "do")
TOKEN_WHILE = Category("while", "while")
TOKEN_BREAK = Category("break", "break")
TOKEN_CONTINUE = Category("continue", "continue")
TOKEN_RETURN = Category("return", "return")


# Type
TOKEN_INT = Category("int", "int")
TOKEN_VOID = Category("void", "void")


# Bracket
TOKEN_PARENTHESIS_OPEN = Category("opening parenthesis", "(")
TOKEN_PARENTHESIS_CLOSE = Category("closing parenthesis", ")")

TOKEN_CURLY_BRACKET_OPEN = Category("opening curly bracket", "{")
TOKEN_CURLY_BRACKET_CLOSE = Category("closing curly bracket", "}")

TOKEN_SQUARE_BRACKET_OPEN = Category("opening square bracket", "[")
TOKEN_SQUARE_BRACKET_CLOSE = Category("closing square bracket", "]")


# Operator
TOKEN_PLUS = Category("plus", "+")
TOKEN_MINUS = Category("minus", "-")
TOKEN_MULTIPLICATION = Category("multiplication", "*")
TOKEN_DIVIDER = Category("divider", "/")
TOKEN_MODULO = Category("modulo", "%")


# Comparator
TOKEN_EQUALS = Category("equals", "==")
TOKEN_NOT_EQUALS = Category("not equals", "!=")

TOKEN_LOWER_THAN = Category("lower than", "<")
TOKEN_GREATER_THAN = Category("greater than", ">")

TOKEN_LOWER_EQUALS_THAN = Category("lower equals than", "<=")
TOKEN_GREATER_EQUALS_THAN = Category("greater equals than", ">=")


# Condition operator
TOKEN_AND = Category("and", "&&")
TOKEN_OR = Category("or", "||")
TOKEN_NOT = Category("not", "!")


# Pointer
TOKEN_POINTER_ADRESS = Category("pointer adress", "&")
TOKEN_POINTER_VALUE = Category("pointer value", "@")


# Other
TOKEN_SEMICOLON = Category("semicolon", ";")
TOKEN_AFFECT = Category("affectation", "=")
TOKEN_IDENT = Category("identifiant", "^[a-zA-Z][a-zA-Z0-9]*")
TOKEN_VALUE = Category("value", "[0-9]+")


ALL_TOKENS = [
    TOKEN_IF,
    TOKEN_ELSE,
    TOKEN_FOR,
    TOKEN_DO,
    TOKEN_WHILE,
    TOKEN_BREAK,
    TOKEN_CONTINUE,
    TOKEN_RETURN,
    TOKEN_INT,
    TOKEN_VOID,
    TOKEN_PARENTHESIS_OPEN,
    TOKEN_PARENTHESIS_CLOSE,
    TOKEN_CURLY_BRACKET_OPEN,
    TOKEN_CURLY_BRACKET_CLOSE,
    TOKEN_SQUARE_BRACKET_OPEN,
    TOKEN_SQUARE_BRACKET_CLOSE,
    TOKEN_PLUS,
    TOKEN_MINUS,
    TOKEN_MULTIPLICATION,
    TOKEN_DIVIDER,
    TOKEN_MODULO,
    TOKEN_EQUALS,
    TOKEN_NOT_EQUALS,
    TOKEN_LOWER_THAN,
    TOKEN_GREATER_THAN,
    TOKEN_LOWER_EQUALS_THAN,
    TOKEN_GREATER_EQUALS_THAN,
    TOKEN_AND,
    TOKEN_OR,
    TOKEN_NOT,
    TOKEN_POINTER_ADRESS,
    TOKEN_POINTER_VALUE,
    TOKEN_SEMICOLON,
    TOKEN_AFFECT,
    TOKEN_IDENT,
    TOKEN_VALUE
]

MAP_TOKENS = {cat.symbol: cat for cat in ALL_TOKENS}
