# main.py
import sys
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from repl import REPL

def run_program(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    lexer = Lexer(text)
    parser = Parser(lexer)
    tree = parser.parse()
    interpreter = Interpreter()
    result = interpreter.interpret(tree)
    print(result)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        run_program(sys.argv[1])
    else:
        repl = REPL()
        repl.start()
