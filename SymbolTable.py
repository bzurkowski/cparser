#!/usr/bin/python


class Symbol(object):
    pass


class Fundef(Symbol):

    def __init__(self, name, type, args):
        self.name = name
        self.type = type
        self.args = args


class VariableSymbol(Symbol):

    def __init__(self, name, type):
        self.name = name
        self.type = type


class Scope(object):

    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.entries = dict()

    def put(self, name, symbol):
        self.entries[name] = symbol

    def get(self, name):
        return self.entries[name]

    def has_entry(self, name):
        return self.entries.has_key(name)

    def name(self):
        return self.name


class SymbolTable(object):

    def __init__(self, scope_name):
        root_scope = Scope(None, scope_name)

        self.scopes = dict()
        self.scopes[scope_name] = root_scope
        self.scope = root_scope

    def push_scope(self, scope_name):
        if not self.scopes.has_key(scope_name):
            self.scopes[scope_name] = Scope(self.scope, scope_name)
        self.set_scope(scope_name)

    def pop_scope(self):
        self.set_scope(self.scope.parent.name)

    def set_scope(self, scope_name):
        if self.scopes.has_key(scope_name):
            self.scope = self.scopes[scope_name]

    def put(self, name, symbol):
        self.scopes[self.scope.name].put(name, symbol)

    def get(self, name, scope=None):
        scope_name = scope.name if scope != None else self.scope.name

        if self.exists(name, scope=scope):
            return self.scopes[scope_name].get(name)

    def exists(self, name, scope=None):
        scope_name = scope.name if scope != None else self.scope.name
        return self.scopes[scope_name].has_entry(name)

    def scope_exists(self, scope_name):
        return self.scopes.has_key(scope_name)

    def current_scope(self):
        return self.scope.name

    def find(self, name):
        scope = self.scope
        while scope != None:
            if self.exists(name, scope=scope):
                return self.get(name, scope=scope)
            scope = scope.parent

    def __str__(self):
        s = ""
        for scope_name, scope in self.scopes.iteritems():
            s += str(scope_name) + ':\n'
            for entry in scope.entries:
                s += '\t' + str(entry) + ': ' + str(scope.entries[entry])
        return s
