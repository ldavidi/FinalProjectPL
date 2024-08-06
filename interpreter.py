from ast import *
from lexer import *

class Interpreter:
    def __init__(self):
        self.global_env = {}

    def error(self, message):
        raise Exception(f'Runtime error: {message}')

    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        self.error(f'No visit_{type(node).__name__} method')

    def visit_BinaryOperation(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if node.op.type == PLUS:
            return left + right
        elif node.op.type == MINUS:
            return left - right
        elif node.op.type == MUL:
            return left * right
        elif node.op.type == DIV:
            if right == 0:
                self.error("Division by zero")
            return left // right  # Assuming integer division
        elif node.op.type == MOD:
            if right == 0:
                self.error("Modulo by zero")
            return left % right
        elif node.op.type == AND:
            return left and right
        elif node.op.type == OR:
            return left or right
        elif node.op.type == EQ:
            return left == right
        elif node.op.type == NEQ:
            return left != right
        elif node.op.type == GT:
            return left > right
        elif node.op.type == LT:
            return left < right
        elif node.op.type == GTE:
            return left >= right
        elif node.op.type == LTE:
            return left <= right

    def visit_UnaryOperation(self, node):
        operand = self.visit(node.operand)
        if node.op.type == NOT:
            return not operand

    def visit_Literal(self, node):
        return node.value

    def visit_Variable(self, node):
        name = node.name
        if name in self.global_env:
            return self.global_env[name]
        else:
            self.error(f'Variable {name} not defined')

    def visit_FunctionDefinition(self, node):
        self.global_env[node.name.value] = node

    def visit_LambdaExpression(self, node):
        def func(*args):
            if len(args) != len(node.params):
                self.error(f'Lambda function expected {len(node.params)} arguments, got {len(args)}')
            new_env = self.global_env.copy()
            for param, arg in zip(node.params, args):
                new_env[param.value] = arg
            previous_env = self.global_env
            self.global_env = {**node.env, **new_env}
            result = self.visit(node.body)
            self.global_env = previous_env
            return result

        node.env = self.global_env.copy()
        return func

    def visit_FunctionApplication(self, node):
        func = self.visit(node.func)
        args = [self.visit(arg) for arg in node.args]
        if callable(func):
            return func(*args)
        elif isinstance(func, FunctionDefinition):
            if len(args) != len(func.params):
                self.error(f'Function {func.name.value} expected {len(func.params)} arguments, got {len(args)}')
            new_env = self.global_env.copy()
            for param, arg in zip(func.params, args):
                new_env[param.value] = arg
            previous_env = self.global_env
            self.global_env = new_env
            result = self.visit(func.body)
            self.global_env = previous_env
            return result
        else:
            self.error(f'{node.func} is not a function')

    def visit_IfStatement(self, node):
        condition = self.visit(node.condition)
        if condition:
            return self.visit(node.true_block)
        elif node.false_block:
            return self.visit(node.false_block)
        return None

    def interpret(self, tree):
        result = None
        for node in tree:
            result = self.visit(node)
        return result
