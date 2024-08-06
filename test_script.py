# test_script.py
from lexer import *
from parser import Parser
from interpreter import Interpreter

def test_lexer():
    text = "(lambda x. (lambda y. (x + y)))(3)(4)"
    lexer = Lexer(text)
    token = lexer.get_next_token()
    while token.type != EOF:
        print(token)
        token = lexer.get_next_token()

def test_parser():
    text = "(lambda x. (lambda y. (x + y)))(3)(4)"
    lexer = Lexer(text)
    parser = Parser(lexer)
    tree = parser.parse()
    for node in tree:
        print(node)

def test_interpreter():
    text = "(lambda x. (lambda y. (x + y)))(3)(4)"
    lexer = Lexer(text)
    parser = Parser(lexer)
    tree = parser.parse()
    interpreter = Interpreter()
    result = interpreter.interpret(tree)
    print(result)  # This should print 6

if __name__ == '__main__':
    print("Testing Lexer")
    test_lexer()
    print("\nTesting Parser")
    test_parser()
    print("\nTesting Interpreter")
    test_interpreter()
