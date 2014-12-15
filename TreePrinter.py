
import AST


def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator


class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self, offset=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.Program)
    def printTree(self, offset=0):
        s = '\n'.join([str(d[0]) for d in self.declarations]) + '\n'
        s += '\n'.join([str(f[0]) for f in self.fundefs]) + '\n'
        s += '\n'.join([str(i) for i in self.instructions])
        return s

    @addToClass(AST.Declaration)
    def printTree(self, offset=0):
        lead = '| ' * offset
        s = lead + 'DECL\n'
        s += '\n'.join([i.printTree(offset + 1) for i in self.inits])
        return s

    @addToClass(AST.Init)
    def printTree(self, offset=0):
        lead = '| ' * offset
        s = lead + '=\n'
        s += lead + '| ' + str(self.name) + '\n'
        s += self.expression.printTree(offset + 1)
        return s

    @addToClass(AST.Expression)
    def printTree(self, offset=0):
        return self.content.printTree(offset)

    @addToClass(AST.BinExpr)
    def printTree(self, offset=0):
        lead = '| ' * offset
        s = lead + str(self.op) + '\n'
        s += self.left.printTree(offset + 1) + '\n'
        s += self.right.printTree(offset + 1)
        return s

    @addToClass(AST.Variable)
    def printTree(self, offset=0):
        lead = '| ' * offset
        return lead + str(self.name)

    @addToClass(AST.Fundef)
    def printTree(self, offset=0):
        lead = '| ' * offset
        s = lead + 'FUNDEF\n'
        s += lead + '| ' + str(self.name) + '\n'
        s += lead + '| ' + 'RET ' + str(self.type) + '\n'
        s += '\n'.join([a.printTree(offset + 1) for a in self.args]) + '\n'
        s += self.compound_instr.printTree(offset + 1)
        return s

    @addToClass(AST.Arg)
    def printTree(self, offset=0):
        lead = '| ' * offset
        return lead + 'ARG ' + str(self.name)

    @addToClass(AST.CompoundInstr)
    def printTree(self, offset=0):
        s = '\n'.join([d[0].printTree(offset) for d in self.declarations]) + '\n'
        s += '\n'.join([i.printTree(offset) for i in self.instructions])
        return s

    @addToClass(AST.Const)
    def printTree(self, offset=0):
        lead = '| ' * offset
        return lead + str(self.value)

    @addToClass(AST.WhileInstr)
    def printTree(self, offset=0):
        lead = '| ' * offset
        s = lead + 'WHILE\n'
        s += self.condition.printTree(offset + 1)
        s += self.instruction.printTree(offset + 1)
        return s

    @addToClass(AST.Condition)
    def printTree(self, offset=0):
        return self.expression.printTree(offset)

    @addToClass(AST.Assignment)
    def printTree(self, offset=0):
        lead = '| ' * offset
        s = lead + '=\n'
        s += lead + str(self.name) + '\n'
        s += self.expression.printTree(offset)
        return s

    @addToClass(AST.ChoiceInstr)
    def printTree(self, offset=0):
        lead = '| ' * offset
        s = lead + 'IF\n'
        s += self.condition.printTree(offset + 1) + '\n'
        s += self.yes_instr.printTree(offset + 1)

        if self.no_instr != None:
            s += '\n' + lead + 'ELSE\n'
            s += self.no_instr.printTree(offset + 1)
        return s

    @addToClass(AST.PrintInstr)
    def printTree(self, offset=0):
        lead = '| ' * offset
        s = lead + 'PRINT\n'
        s += self.expression.printTree(offset + 1)
        return s

    @addToClass(AST.ReturnInstr)
    def printTree(self, offset=0):
        lead = '| ' * offset
        s = lead + 'RETURN\n'
        s += self.expression.printTree(offset + 1)
        return s

    @addToClass(AST.Funcall)
    def printTree(self, offset=0):
        lead = '| ' * offset
        s = lead + 'FUNCALL\n'
        s += lead + '| ' + str(self.name)

        if len(self.args) > 0:
            s += '\n' + self.args[0].printTree(offset + 1)
        return s







