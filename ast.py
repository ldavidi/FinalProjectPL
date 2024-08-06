# ast_nodes.py

class AST:
    pass

class BinaryOperation(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class UnaryOperation(AST):
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand

class Literal(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Variable(AST):
    def __init__(self, token):
        self.token = token
        self.name = token.value

class FunctionDefinition(AST):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class LambdaExpression(AST):
    def __init__(self, params, body):
        self.params = params
        self.body = body

class FunctionApplication(AST):
    def __init__(self, func, args):
        self.func = func
        self.args = args

class IfStatement(AST):
    def __init__(self, condition, true_block, false_block):
        self.condition = condition
        self.true_block = true_block
        self.false_block = false_block
