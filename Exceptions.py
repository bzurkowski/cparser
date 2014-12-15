class Error(object):

    def __init__(self, node, msg, lineno=None):
        self.node = node
        self.msg = msg
        self.lineno = lineno if lineno != None else node.lineno

    def __str__(self):
        msg = "ERROR in line {0}: {1}".format(self.lineno, self.msg)
        return msg


class SemanticError(Error):
    pass