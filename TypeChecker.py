#!/usr/bin/python


import AST
import SymbolTable as ST
import TType as TT
from Exceptions import *


class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children():
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)


class TypeChecker(NodeVisitor):

    def __init__(self, node):
        self.symtab = ST.SymbolTable(node.__class__.__name__)
        self.ttype = TT.TType()

    def visit_Program(self, node):
        self.visit(node.declarations)
        self.visit(node.fundefs)
        self.visit(node.instructions)

    def visit_Declaration(self, node):
        decl_type = node.type

        for init in node.inits:
            init_type = self.visit(init)

            if self.ttype.op_not_allowed('=', decl_type, init_type):
                msg = "Types of declaration sides don't match. Left: {0}, right: {1}.".format(decl_type, init_type)
                print SemanticError(node, msg)
            elif self.symtab.exists(init.name):
                msg = "Multiple declaration of variable '{0}' in current scope '{1}'.".format(init.name, self.symtab.current_scope())
                print SemanticError(node, msg)
            else:
                self.symtab.put(init.name, ST.VariableSymbol(init.name, init_type))

    def visit_Init(self, node):
        return self.visit(node.expression)

    def visit_Assignment(self, node):
        sym = self.symtab.find(node.name)

        if sym == None:
            msg = "Variable '{0}' not declared.".format(node.name)
            print SemanticError(node, msg)

    def visit_CompoundInstr(self, node):
        self.visit(node.declarations)
        self.visit(node.instructions)

    def visit_BinExpr(self, node):
        type_a = self.visit(node.left)
        type_b = self.visit(node.right)
        op = node.op
        return self.ttype.get(op, type_a, type_b)

    def visit_Integer(self, node):
        return 'int'

    def visit_Float(self, node):
        return 'float'

    def visit_String(self, node):
        return 'string'

    def visit_Variable(self, node):
        sym = self.symtab.find(node.name)

        if sym != None:
            return sym.type
        else:
            msg = "Variable '{0}' not declared.".format(node.name)
            print SemanticError(node, msg)

    def visit_Funcall(self, node):
        fundef = self.symtab.find(node.name)

        if fundef == None:
            msg = "Function '{0}' not declared in any outer scope.".format(node.name)
            print SemanticError(node, msg)
        elif len(node.args) != len(fundef.args):
            required = len(fundef.args)
            given = len(node.args)

            msg = "Function '{0}' requires {1} arguments, {2} given.".format(node.name, required, given)
            print SemanticError(node, msg)
        else:
            for i in xrange(len(node.args)):
                call_type = self.visit(node.args[i])
                def_type = fundef.args[i].type

                if call_type != def_type:
                    msg = "Given arguments for function '{0}' don't match parameter types in function definition.".format(node.name)
                    print SemanticError(node, msg)
        return fundef.type

    def visit_Fundef(self, node):
        if self.symtab.scope_exists(node.name):
            msg = "Multiple definition of function '{0}'".format(node.name)
            print SemanticError(node, msg)

        self.symtab.put(node.name, ST.Fundef(node.name, node.type, node.args))

        self.symtab.push_scope(node.name)

        self.visit(node.args)
        self.visit(node.compound_instr)

        self.symtab.pop_scope()

    def visit_Arg(self, node):
        if self.symtab.exists(node.name):
            msg = "Multiple definition of same argument for funciton '{0}' in current scope '{1}'.".format(node.name, self.symtab.current_scope())
            print SemanticError(node, msg)
        else:
            self.symtab.put(node.name, ST.VariableSymbol(node.name, node.type))

