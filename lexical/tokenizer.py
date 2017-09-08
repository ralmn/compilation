import lexical


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

            if currentSymbol in lexical.categories_const.MAP_TOKENS:
                tokens.append(lexical.Token(lexical.categories_const.MAP_TOKENS[currentSymbol], line, column))
            else:
                tokens.append(
                    lexical.Token(lexical.categories_const.TOKEN_IDENT, line, column, identifier=currentSymbol))

            column += (charIndexEnd - charIndex)
            charIndex = charIndexEnd
            continue
        elif str.isdigit(c):
            charIndexEnd = charIndex

            while charIndexEnd < nbChar and str.isdigit(input_str[charIndexEnd]):
                charIndexEnd += 1

            currentSymbol = input_str[charIndex:charIndexEnd]
            tokens.append(lexical.Token(lexical.categories_const.TOKEN_VALUE, line, column, value=currentSymbol))

            column += (charIndexEnd - charIndex)
            charIndex = charIndexEnd
            continue
        else:

            if c in lexical.categories_const.MAP_TOKENS:
                category = lexical.categories_const.MAP_TOKENS[c]
                if category in lexical.categories_const.TOKEN_MULTI_CHARS:
                    pass
                else:
                    tokens.append(lexical.Token(category, line, column) )


        charIndex += 1
        column += 1
    return tokens
