# lexer.py
import re

# Token types
INTEGER = 'INTEGER'
BOOLEAN = 'BOOLEAN'
PLUS = 'PLUS'
MINUS = 'MINUS'
MUL = 'MUL'
DIV = 'DIV'
MOD = 'MOD'
AND = 'AND'
OR = 'OR'
NOT = 'NOT'
EQ = 'EQ'
NEQ = 'NEQ'
GT = 'GT'
LT = 'LT'
GTE = 'GTE'
LTE = 'LTE'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
DEFUN = 'DEFUN'
LAMBDA = 'LAMBDA'
IDENTIFIER = 'IDENTIFIER'
EOF = 'EOF'
COMMA = 'COMMA'
IF = 'IF'
ELSE = 'ELSE'

# Token definition
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f'Token({self.type}, {repr(self.value)})'

    def __repr__(self):
        return self.__str__()

# Lexer definition
class Lexer:
    keywords = {
        'defun': DEFUN,
        'lambda': LAMBDA,
        'if': IF,
        'else': ELSE,
        'True': BOOLEAN,
        'False': BOOLEAN,
    }

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
        self.line = 1
        self.column = 1

    def advance(self):
        if self.current_char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def _id(self):
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        token_type = self.keywords.get(result, IDENTIFIER)
        if token_type == BOOLEAN:
            return Token(token_type, result == 'True')
        return Token(token_type, result)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char.isalpha():
                return self._id()

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')

            if self.current_char == '%':
                self.advance()
                return Token(MOD, '%')

            if self.current_char == '&':
                self.advance()
                if self.current_char == '&':
                    self.advance()
                    return Token(AND, '&&')
                else:
                    self.error()

            if self.current_char == '|':
                self.advance()
                if self.current_char == '|':
                    self.advance()
                    return Token(OR, '||')
                else:
                    self.error()

            if self.current_char == '!':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(NEQ, '!=')
                else:
                    return Token(NOT, '!')

            if self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(EQ, '==')
                else:
                    self.error()

            if self.current_char == '>':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(GTE, '>=')
                else:
                    return Token(GT, '>')

            if self.current_char == '<':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(LTE, '<=')
                else:
                    return Token(LT, '<')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            if self.current_char == ',':
                self.advance()
                return Token(COMMA, ',')

            if self.current_char == '{':
                self.advance()
                return Token('{', '{')

            if self.current_char == '}':
                self.advance()
                return Token('}', '}')

            self.error()

        return Token(EOF, None)

    def error(self):
        raise Exception(f'Lexer error at position {self.pos}: Invalid character {self.current_char}')
