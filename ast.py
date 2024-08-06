class AST:
    pass


class BinaryOperation(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __str__(self):
        return f'({self.left} {self.op.value} {self.right})'

    def __repr__(self):
        return self.__str__()


class UnaryOperation(AST):
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand

    def __str__(self):
        return f'({self.op.value} {self.operand})'

    def __repr__(self):
        return self.__str__()


class Literal(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return self.__str__()


class Variable(AST):
    def __init__(self, token):
        self.token = token
        self.name = token.value

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class FunctionDefinition(AST):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def __str__(self):
        return f'defun {self.name.value}({", ".join(param.value for param in self.params)}) {{ {self.body} }}'

    def __repr__(self):
        return self.__str__()


class LambdaExpression(AST):
    def __init__(self, params, body):
        self.params = params
        self.body = body
        self.env = None  # Store the environment where the lambda is defined
    def __str__(self):
        return f'lambda {", ".join(param.value for param in self.params)}. {self.body}'

    def __repr__(self):
        return self.__str__()


class FunctionApplication(AST):
    def __init__(self, func, args):
        self.func = func
        self.args = args

    def __str__(self):
        return f'{self.func}({", ".join(str(arg) for arg in self.args)})'

    def __repr__(self):
        return self.__str__()


class IfStatement(AST):
    def __init__(self, condition, true_block, false_block):
        self.condition = condition
        self.true_block = true_block
        self.false_block = false_block

    def __str__(self):
        return f'if ({self.condition}) {{ {self.true_block} }} else {{ {self.false_block} }}'

    def __repr__(self):
        return self.__str__()
