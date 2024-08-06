# repl.py
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

class REPL:
    def __init__(self):
        self.lexer = None
        self.parser = None
        self.interpreter = Interpreter()

    def start(self):
        print("Welcome to the Functional Language Interpreter REPL. Type 'exit' to quit.")
        while True:
            try:
                text = input('>>> ')
                if text.strip().lower() == 'exit':
                    break
                self.lexer = Lexer(text)
                self.parser = Parser(self.lexer)
                tree = self.parser.parse()
                result = self.interpreter.interpret(tree)
                print(result)
            except Exception as e:
                print(f'Error: {e}')
