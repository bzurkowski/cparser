
class Node(object):

    def __init__(self, lineno):
        self.lineno = lineno

    def __str__(self):
        return self.printTree()

    def children(self):
        return tuple()


class Program(Node):

    def __init__(self, lineno, declarations, fundefs, instructions):
        self.declarations = declarations
        self.fundefs = fundefs
        self.instructions = instructions
        self.lineno = lineno

    def children(self):
        nodes = [self.declarations, self.fundefs, self.instructions]
        return tuple(nodes)


class Declaration(Node):

    def __init__(self, lineno, type, inits):
        self.type = type
        self.inits = inits
        self.lineno = lineno

    def children(self):
        nodes = [self.inits]
        return tuple(nodes)


class Expression(Node):
    pass


class Init(Node):

    def __init__(self, lineno, name, expression):
        self.name = name
        self.expression = expression
        self.lineno = lineno

    def children(self):
        nodes = [self.expression]
        return tuple(nodes)


class Instruction(Node):
    pass


class PrintInstr(Instruction):

    def __init__(self, lineno, expression):
        self.expression = expression
        self.lineno = lineno

    def children(self):
        nodes = [self.expression]
        return tuple(nodes)


class LabeledInstr(Node):

    def __init__(self, lineno, id, instruction):
        self.id = id
        self.instruction = instruction
        self.lineno = lineno

    def children(self):
        nodes = [self.instruction]
        return tuple(nodes)


class Assignment(Instruction):

    def __init__(self, lineno, name, expression):
        self.name = name
        self.expression = expression
        self.lineno = lineno

    def children(self):
        nodes = [self.expression]
        return tuple(nodes)


class ChoiceInstr(Instruction):

    def __init__(self, lineno, condition, yes_instr, no_instr=None):
        self.condition = condition
        self.yes_instr = yes_instr
        self.no_instr = no_instr
        self.lineno = lineno

    def children(self):
        nodes = [self.condition, self.yes_instr]
        if self.no_instr != None: nodes.append(self.no_instr)
        return tuple(nodes)


class LoopInstr(Instruction):

    def __init__(self, lineno, condition, instruction):
        self.condition = condition
        self.instruction = instruction
        self.lineno = lineno

    def children(self):
        nodes = [self.condition, self.instruction]
        return tuple(nodes)


class WhileInstr(LoopInstr):
    pass


class RepeatInstr(LoopInstr):
    pass


class InterruptInstr(Instruction):

    def children(self):
        return tuple()


class ReturnInstr(InterruptInstr):

    def __init__(self, lineno, expression):
        self.expression = expression
        self.lineno = lineno

    def children(self):
        nodes = [self.expression]
        return tuple(nodes)


class ContinueInstr(InterruptInstr):
    pass


class BreakInstr(InterruptInstr):
    pass


class CompoundInstr(Instruction):

    def __init__(self, lineno, declarations, instructions):
        self.declarations = declarations
        self.instructions = instructions
        self.lineno = lineno

    def children(self):
        nodes = [self.declarations, self.instructions]
        return tuple(nodes)


class Condition(Node):

    def __init__(self, lineno, expression):
        self.expression = expression
        self.lineno = lineno

    def children(self):
        nodes = [self.expression]
        return tuple(nodes)


class Const(Expression):

    def __init__(self, lineno, value):
        self.value = value
        self.lineno = lineno

    def children(self):
        return tuple()


class Integer(Const):
    pass


class Float(Const):
    pass


class String(Const):
    pass


class Variable(Node):

    def __init__(self, lineno, type, name):
        self.type = type
        self.name = name
        self.lineno = lineno


class BinExpr(Expression):

    def __init__(self, lineno, op, left, right):
        self.op = op
        self.left = left
        self.right = right
        self.lineno = lineno

    def children(self):
        nodes = [self.left, self.right]
        return tuple(nodes)


class Funcall(Expression):

    def __init__(self, lineno, name, args):
        self.name = name
        self.args = args
        self.lineno = lineno

    def children(self):
        nodes = [self.args]
        return tuple(nodes)


class Fundef(Node):

    def __init__(self, lineno, type, name, args, compound_instr):
        self.type = type
        self.name = name
        self.args = args
        self.compound_instr = compound_instr
        self.lineno = lineno

    def children(self):
        nodes = [self.args, self.compound_instr]
        return tuple(nodes)


class Arg(Variable):
    pass


