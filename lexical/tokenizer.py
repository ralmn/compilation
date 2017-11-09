import categories_const
from token import Token


def tokenize(input_str):
    """
    :param input_str: Chaine entree
    :return: listes des tokens
    """
    charIndex = 0
    line = 1
    column = 1

    nbChar = len(input_str)
    tokens = []
    while charIndex < nbChar:
        c = input_str[charIndex]

        if ord(c) == 13:  # 13 = \r
            column = 1
            charIndex += 1
            continue
        elif ord(c) == 10:  # 10 = '\n'
            line += 1
            column = 1
            charIndex += 1
            continue
        elif str.isspace(c):
            charIndex += 1
            column += 1
            continue

        if str.isalpha(c):

            charIndexEnd = charIndex
            while charIndexEnd < nbChar and str.isalnum(input_str[charIndexEnd]):
                charIndexEnd += 1

            currentSymbol = input_str[charIndex:charIndexEnd]

            if currentSymbol in categories_const.MAP_TOKENS:
                tokens.append(Token(categories_const.MAP_TOKENS[currentSymbol], line, column))
            else:
                tokens.append(
                    Token(categories_const.TOKEN_IDENT, line, column, identifier=currentSymbol))

            column += (charIndexEnd - charIndex)
            charIndex = charIndexEnd
            continue
        elif str.isdigit(c):
            charIndexEnd = charIndex

            while charIndexEnd < nbChar and str.isdigit(input_str[charIndexEnd]):
                charIndexEnd += 1

            currentSymbol = input_str[charIndex:charIndexEnd]
            tokens.append(Token(categories_const.TOKEN_VALUE, line, column, value=int(currentSymbol)))

            column += (charIndexEnd - charIndex)
            charIndex = charIndexEnd
            continue
        else:

            if c in categories_const.MAP_TOKENS:
                category = categories_const.MAP_TOKENS[c]
                if category in categories_const.TOKEN_MULTI_CHARS:

                    if len(input_str) > charIndex + 1:
                        currentSymbol = input_str[charIndex:charIndex+2]
                        if currentSymbol in categories_const.MAP_TOKENS:
                            category = categories_const.MAP_TOKENS[currentSymbol]
                            tokens.append(Token(category, line, column))
                            charIndex += 2
                            column += 2
                            continue



                tokens.append(Token(category, line, column) )

            elif c in categories_const.TOKEN_UNIQUE_MULTI_CHARS:
                charOffset = 1
                while len(input_str) > charIndex + charOffset:
                    currentSymbol = input_str[charIndex:charIndex + (charOffset + 1)]

                    if currentSymbol in categories_const.MAP_TOKENS:
                        category = categories_const.MAP_TOKENS[currentSymbol]
                        tokens.append(Token(category, line, column))
                        charIndex += charOffset
                        column += charOffset
                        break

        charIndex += 1
        column += 1
    return tokens
