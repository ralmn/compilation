class CompileException(Exception):

    str = ""

    def __init__(self, message, token=None, line=None):

        # Now for your custom code...
        tmp_message = ""
        if token is not None:
            tmp_message += "Error line " + str(token.line) + ": \r\n"
            tmp_message += getLineError(token.line) + "\r\n"
            for i in range(token.column - 1):
                tmp_message += " "
            tmp_message += "^\r\n"
        else:
            if line is not None:
                tmp_message += "Error line " + str(line) + ": \r\n"
                tmp_message += getLineError(line) + "\r\n"
        super(CompileException, self).__init__(tmp_message + message)



def getLineError(line):
    tmp_tab = CompileException.str.split("\n", line)
    return tmp_tab[len(tmp_tab)-2]