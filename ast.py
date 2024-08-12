class AST:
    """Base class for all Abstract Syntax Tree (AST) nodes."""
    pass


class BinaryOperation(AST):
    """Represents a binary operation (e.g., addition, subtraction)."""

    def __init__(self, left, operator, right):
        self.left = left  # Left operand
        self.operator = operator  # Operator (e.g., +, -, *)
        self.right = right  # Right operand

    def __str__(self):
        return f'({self.left} {self.operator.value} {self.right})'

    def __repr__(self):
        return self.__str__()


class UnaryOperation(AST):
    """Represents a unary operation (e.g., negation, logical NOT)."""

    def __init__(self, operator, operand):
        self.operator = operator  # Operator (e.g., NOT)
        self.operand = operand  # Operand

    def __str__(self):
        return f'({self.operator.value} {self.operand})'

    def __repr__(self):
        return self.__str__()


class Literal(AST):
    """Represents a literal value (e.g., integer, boolean)."""

    def __init__(self, token):
        self.token = token
        self.value = token.value  # Value of the literal

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return self.__str__()


class Variable(AST):
    """Represents a variable."""

    def __init__(self, token):
        self.token = token
        self.name = token.value  # Name of the variable

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class FunctionDefinition(AST):
    """Represents a function definition."""

    def __init__(self, name, parameters, body):
        self.name = name  # Function name
        self.parameters = parameters  # Function parameters
        self.body = body  # List of expressions in the function body

    def __str__(self):
        params_str = ", ".join(param.value for param in self.parameters)
        body_str = " ".join(str(expr) for expr in self.body)
        return f'defun {self.name.value}({params_str}) {{ {body_str} }}'

    def __repr__(self):
        return self.__str__()


class LambdaExpression(AST):
    """Represents a lambda expression."""

    def __init__(self, parameters, body):
        self.parameters = parameters  # Lambda parameters
        self.body = body  # Lambda body (a single expression)
        self.env = None  # Store the environment where the lambda is defined

    def __str__(self):
        params_str = ", ".join(param.value for param in self.parameters)
        return f'lambda {params_str}. {self.body}'

    def __repr__(self):
        return self.__str__()


class FunctionApplication(AST):
    """Represents a function or lambda application."""

    def __init__(self, func, arguments):
        self.func = func  # Function or lambda to be applied
        self.arguments = arguments  # Arguments for the function or lambda

    def __str__(self):
        args_str = ", ".join(str(arg) for arg in self.arguments)
        return f'{self.func}({args_str})'

    def __repr__(self):
        return self.__str__()


class IfStatement(AST):
    """Represents an if-else statement."""

    def __init__(self, condition, true_block, false_block=None):
        self.condition = condition  # Condition expression
        self.true_block = true_block  # List of expressions in the true block
        self.false_block = false_block  # List of expressions in the false block (optional)

    def __str__(self):
        true_block_str = " ".join(str(expr) for expr in self.true_block)
        false_block_str = " ".join(str(expr) for expr in self.false_block) if self.false_block else ""
        return f'if ({self.condition}) {{ {true_block_str} }} else {{ {false_block_str} }}'

    def __repr__(self):
        return self.__str__()


class PrintStatement(AST):
    """Represents a print statement."""

    def __init__(self, expression):
        self.expression = expression  # Expression to be printed

    def __str__(self):
        return f'print({self.expression})'

    def __repr__(self):
        return self.__str__()
