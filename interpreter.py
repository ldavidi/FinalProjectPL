from ast import *
from lexer import *

class Interpreter:
    """Interpreter for executing the Abstract Syntax Tree (AST)."""

    def __init__(self):
        self.global_env = {}

    def error(self, message):
        """Raise a runtime error with a custom message."""
        raise Exception(f'Runtime error: {message}')

    def visit(self, node):
        """Visit a node in the AST and execute the corresponding method."""
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """Fallback method if no explicit visitor function is found."""
        self.error(f'No visit_{type(node).__name__} method')

    def visit_BinaryOperation(self, node):
        """Evaluate a binary operation (e.g., +, -, *, /)."""
        left_value = self.visit(node.left)
        right_value = self.visit(node.right)
        operator = node.operator.type

        if operator == PLUS:
            return left_value + right_value
        elif operator == MINUS:
            return left_value - right_value
        elif operator == MUL:
            return left_value * right_value
        elif operator == DIV:
            if right_value == 0:
                self.error("Division by zero")
            return left_value // right_value  # Assuming integer division
        elif operator == MOD:
            if right_value == 0:
                self.error("Modulo by zero")
            return left_value % right_value
        elif operator == AND:
            return left_value and right_value
        elif operator == OR:
            return left_value or right_value
        elif operator == EQ:
            return left_value == right_value
        elif operator == NEQ:
            return left_value != right_value
        elif operator == GT:
            return left_value > right_value
        elif operator == LT:
            return left_value < right_value
        elif operator == GTE:
            return left_value >= right_value
        elif operator == LTE:
            return left_value <= right_value

    def visit_UnaryOperation(self, node):
        """Evaluate a unary operation (e.g., NOT)."""
        operand_value = self.visit(node.operand)
        if node.operator.type == NOT:
            return not operand_value

    def visit_Literal(self, node):
        """Return the value of a literal (e.g., integer, boolean)."""
        return node.value

    def visit_Variable(self, node):
        """Return the value of a variable."""
        variable_name = node.name
        if variable_name in self.global_env:
            return self.global_env[variable_name]
        else:
            self.error(f'Variable {variable_name} not defined')

    def visit_FunctionDefinition(self, node):
        """Store a function definition in the global environment."""
        self.global_env[node.name.value] = node

    def visit_FunctionApplication(self, node):
        """Apply a function or lambda with arguments."""
        func = self.visit(node.func)
        args = [self.visit(arg) for arg in node.arguments]

        if callable(func):
            return func(*args)
        elif isinstance(func, FunctionDefinition):
            if len(args) != len(func.parameters):
                self.error(f'Function {func.name.value} expected {len(func.parameters)} arguments, got {len(args)}')
            new_env = self.global_env.copy()
            for param, arg in zip(func.parameters, args):
                new_env[param.value] = arg
            previous_env = self.global_env
            self.global_env = new_env
            result = None
            for expr in func.body:  # Iterate over the list of expressions
                result = self.visit(expr)
            self.global_env = previous_env
            return result
        else:
            self.error(f'{node.func} is not a function')

    def visit_LambdaExpression(self, node):
        """Return a callable lambda function."""
        def lambda_function(*args):
            if len(args) != len(node.parameters):
                self.error(f'Lambda function expected {len(node.parameters)} arguments, got {len(args)}')
            new_env = self.global_env.copy()
            for param, arg in zip(node.parameters, args):
                new_env[param.value] = arg
            previous_env = self.global_env
            self.global_env = {**node.env, **new_env}
            result = self.visit(node.body)
            self.global_env = previous_env
            return result

        node.env = self.global_env.copy()
        return lambda_function

    def visit_IfStatement(self, node):
        """Evaluate an if-else statement."""
        result = None
        condition_value = self.visit(node.condition)
        if condition_value:
            for expr in node.true_block:
                result = self.visit(expr)
        elif node.false_block:
            for expr in node.false_block:
                result = self.visit(expr)
        return result

    def visit_PrintStatement(self, node):
        """Evaluate a print statement."""
        value = self.visit(node.expression)
        print(value)

    def interpret(self, tree):
        """Interpret the AST starting from the root."""
        result = None
        for node in tree:
            result = self.visit(node)
        return result
