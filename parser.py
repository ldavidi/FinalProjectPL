# parser.py
from lexer import *
from ast import *

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, message):
        raise Exception(f'Parser error: {message} at token {self.current_token}')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f'Expected token {token_type}, got {self.current_token.type}')

    def peek(self):
        pos = self.lexer.pos
        current_char = self.lexer.current_char
        token = self.lexer.get_next_token()
        self.lexer.pos = pos
        self.lexer.current_char = current_char
        return token

    def function_definition(self):
        self.eat(DEFUN)
        name = self.current_token
        self.eat(IDENTIFIER)
        self.eat(LPAREN)
        params = []
        while self.current_token.type != RPAREN:
            param = self.current_token
            self.eat(IDENTIFIER)
            params.append(param)
            if self.current_token.type == COMMA:
                self.eat(COMMA)
        self.eat(RPAREN)
        self.eat('{')
        body = self.expr()
        self.eat('}')
        return FunctionDefinition(name, params, body)

    def lambda_expression(self):
        self.eat(LAMBDA)
        self.eat(LPAREN)
        params = []
        while self.current_token.type != RPAREN:
            param = self.current_token
            self.eat(IDENTIFIER)
            params.append(param)
            if self.current_token.type == COMMA:
                self.eat(COMMA)
        self.eat(RPAREN)
        body = self.expr()
        return LambdaExpression(params, body)

    def function_application(self):
        func_name = self.current_token
        func = self.current_token
        self.eat(IDENTIFIER)
        self.eat(LPAREN)
        args = []
        while self.current_token.type != RPAREN:
            args.append(self.expr())
            if self.current_token.type == COMMA:
                self.eat(COMMA)
        self.eat(RPAREN)
        return FunctionApplication(Variable(func_name), args)

    def if_statement(self):
        self.eat(IF)
        self.eat(LPAREN)
        condition = self.expr()
        self.eat(RPAREN)
        self.eat('{')
        true_block = self.expr()
        self.eat('}')
        if self.current_token.type == ELSE:
            self.eat(ELSE)
            self.eat('{')
            false_block = self.expr()
            self.eat('}')
        else:
            false_block = None
        return IfStatement(condition, true_block, false_block)

    def factor(self):
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return Literal(token)
        elif token.type == BOOLEAN:
            self.eat(BOOLEAN)
            return Literal(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        elif token.type == NOT:
            self.eat(NOT)
            node = UnaryOperation(token, self.factor())
            return node
        elif token.type == IDENTIFIER and self.peek().type == LPAREN:
            return self.function_application()
        elif token.type == IDENTIFIER:
            var = Variable(token)
            self.eat(IDENTIFIER)
            return var
        elif token.type == DEFUN:
            return self.function_definition()
        elif token.type == LAMBDA:
            return self.lambda_expression()
        elif token.type == IF:
            return self.if_statement()
        self.error('Unexpected token')

    def term(self):
        node = self.factor()

        while self.current_token.type in (MUL, DIV, MOD):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)
            elif token.type == MOD:
                self.eat(MOD)

            node = BinaryOperation(left=node, op=token, right=self.factor())

        return node

    def expr(self):
        node = self.term()

        while self.current_token.type in (PLUS, MINUS, AND, OR, EQ, NEQ, GT, LT, GTE, LTE):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)
            elif token.type == AND:
                self.eat(AND)
            elif token.type == OR:
                self.eat(OR)
            elif token.type == EQ:
                self.eat(EQ)
            elif token.type == NEQ:
                self.eat(NEQ)
            elif token.type == GT:
                self.eat(GT)
            elif token.type == LT:
                self.eat(LT)
            elif token.type == GTE:
                self.eat(GTE)
            elif token.type == LTE:
                self.eat(LTE)

            node = BinaryOperation(left=node, op=token, right=self.term())

        return node

    def program(self):
        nodes = []
        while self.current_token.type != EOF:
            if self.current_token.type == DEFUN:
                nodes.append(self.function_definition())
            else:
                nodes.append(self.expr())
        return nodes

    def parse(self):
        return self.program()