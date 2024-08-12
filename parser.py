from lexer import *
from ast import *

class Parser:
    """Parser that constructs an Abstract Syntax Tree (AST) from tokens."""

    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, message):
        """Raise a syntax error with a custom message."""
        raise Exception(f'Parser error: {message} at token {self.current_token}')

    def eat(self, token_type):
        """Consume the current token if it matches the expected type."""
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f'Expected token {token_type}, got {self.current_token.type}')

    def peek(self):
        """Look ahead to the next token without consuming the current one."""
        pos = self.lexer.pos
        current_char = self.lexer.current_char
        next_token = self.lexer.get_next_token()
        self.lexer.pos = pos
        self.lexer.current_char = current_char
        return next_token

    def parse_function_definition(self):
        """Parse a function definition."""
        self.eat(DEFUN)
        name = self.current_token
        self.eat(IDENTIFIER)
        self.eat(LPAREN)
        parameters = []
        while self.current_token.type != RPAREN:
            param = self.current_token
            self.eat(IDENTIFIER)
            parameters.append(param)
            if self.current_token.type == COMMA:
                self.eat(COMMA)
        self.eat(RPAREN)
        self.eat('{')

        # Parsing multiple expressions in the function body
        body = []
        while self.current_token.type != '}':
            body.append(self.parse_expression())

        self.eat('}')
        return FunctionDefinition(name, parameters, body)

    def parse_lambda_expression(self):
        """Parse a lambda expression."""
        self.eat(LAMBDA)
        parameters = []
        while self.current_token.type == IDENTIFIER:
            param = self.current_token
            self.eat(IDENTIFIER)
            parameters.append(param)
            if self.current_token.type == COMMA:
                self.eat(COMMA)
        self.eat(PERIOD)
        body = self.parse_expression()
        return LambdaExpression(parameters, body)

    def parse_function_application(self, func_node=None):
        """Parse a function or lambda application."""
        if not func_node:
            func_name = self.current_token
            func_node = Variable(func_name)
            self.eat(IDENTIFIER)
        self.eat(LPAREN)
        arguments = []
        while self.current_token.type != RPAREN:
            arguments.append(self.parse_expression())
            if self.current_token.type == COMMA:
                self.eat(COMMA)
        self.eat(RPAREN)
        return FunctionApplication(func_node, arguments)

    def parse_if_statement(self):
        """Parse an if-else statement."""
        self.eat(IF)
        self.eat(LPAREN)
        condition = self.parse_expression()
        self.eat(RPAREN)
        self.eat('{')
        true_block = []
        while self.current_token.type != '}':
            true_block.append(self.parse_expression())
        self.eat('}')
        if self.current_token.type == ELSE:
            self.eat(ELSE)
            self.eat('{')
            false_block = []
            while self.current_token.type != '}':
                false_block.append(self.parse_expression())
            self.eat('}')
        else:
            false_block = None
        return IfStatement(condition, true_block, false_block)

    def parse_factor(self):
        """Parse a factor, the simplest form of an expression."""
        token = self.current_token
        if token.type == PRINT:
            self.eat(PRINT)
            expr = self.parse_expression()
            return PrintStatement(expr)
        if token.type == INTEGER:
            self.eat(INTEGER)
            return Literal(token)
        elif token.type == BOOLEAN:
            self.eat(BOOLEAN)
            return Literal(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            expr_node = self.parse_expression()
            self.eat(RPAREN)
            while self.current_token.type == LPAREN:
                expr_node = self.parse_function_application(expr_node)
            return expr_node
        elif token.type == NOT:
            self.eat(NOT)
            node = UnaryOperation(token, self.parse_factor())
            return node
        elif token.type == IDENTIFIER and self.peek().type == LPAREN:
            return self.parse_function_application()
        elif token.type == IDENTIFIER:
            var_node = Variable(token)
            self.eat(IDENTIFIER)
            return var_node
        elif token.type == DEFUN:
            return self.parse_function_definition()
        elif token.type == LAMBDA:
            lambda_node = self.parse_lambda_expression()
            if self.current_token.type == LPAREN:
                lambda_node = self.parse_function_application(lambda_node)
            return lambda_node
        elif token.type == IF:
            return self.parse_if_statement()
        self.error('Unexpected token')

    def parse_term(self):
        """Parse a term, which can be a factor or a product/division/modulo operation."""
        node = self.parse_factor()
        while self.current_token.type in (MUL, DIV, MOD):
            operator = self.current_token
            if operator.type == MUL:
                self.eat(MUL)
            elif operator.type == DIV:
                self.eat(DIV)
            elif operator.type == MOD:
                self.eat(MOD)
            node = BinaryOperation(left=node, operator=operator, right=self.parse_factor())
        return node

    def parse_expression(self):
        """Parse an expression, which can be a term or a complex operation."""
        node = self.parse_term()
        while self.current_token.type in (PLUS, MINUS, AND, OR, EQ, NEQ, GT, LT, GTE, LTE):
            operator = self.current_token
            if operator.type == PLUS:
                self.eat(PLUS)
            elif operator.type == MINUS:
                self.eat(MINUS)
            elif operator.type == AND:
                self.eat(AND)
            elif operator.type == OR:
                self.eat(OR)
            elif operator.type == EQ:
                self.eat(EQ)
            elif operator.type == NEQ:
                self.eat(NEQ)
            elif operator.type == GT:
                self.eat(GT)
            elif operator.type == LT:
                self.eat(LT)
            elif operator.type == GTE:
                self.eat(GTE)
            elif operator.type == LTE:
                self.eat(LTE)
            node = BinaryOperation(left=node, operator=operator, right=self.parse_term())
        return node

    def parse_program(self):
        """Parse the entire program, which consists of multiple expressions."""
        nodes = []
        while self.current_token.type != EOF:
            nodes.append(self.parse_expression())
        return nodes

    def parse(self):
        """Start parsing the program."""
        return self.parse_program()
