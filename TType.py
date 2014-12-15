class TType(object):

    ttype = {
            '+': {
                'int': {
                    'int': 'int',
                    'float': 'float'
                },
                'float': {
                    'int': 'float',
                    'float': 'float'
                },
                'string': {
                    'string': 'string'
                }
            },
            '/': {
                'int': {
                    'int': 'int'
                }
            },
            '*': {
                'int': {
                    'int': 'int'
                }
            },
            '!=': {
                'int': {
                    'int': 'int',
                    'float': 'int'
                },
                'float': {
                    'int': 'int',
                    'float': 'int'
                }
            },
            '=': {
                'int': {
                    'int': 'int'
                },
                'float': {
                    'float': 'float',
                    'int': 'float'
                },
                'string': {
                    'string': 'string'
                }
            },
            '>=': {
                'float': {
                    'float': 'int'
                },
                'int': {
                    'int': 'int'
                }
            },
            '>': {
                'float': {
                    'float': 'int'
                },
                'int': {
                    'int': 'int'
                }
            },
            '-': {
                'float': {
                    'float': 'float'
                },
                'int': {
                    'int': 'int'
                }
            }
        }

    def get(self, op, arg1, arg2):
        if self.op_allowed(op, arg1, arg2):
            return self.ttype[op][arg1][arg2]

    def op_allowed(self, op, arg1, arg2):
        try:
            x = self.ttype[op][arg1][arg2]
        except KeyError:
            return False
        return True

    def op_not_allowed(self, op, arg1, arg2):
        return not self.op_allowed(op, arg1, arg2)
