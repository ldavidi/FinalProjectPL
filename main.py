import sys
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from repl import REPL


def run_program(file_path):
    """
    Read and execute a program from a given file.

    Args:
        file_path (str): Path to the file containing the program to execute.
    """
    with open(file_path, 'r') as file:
        text = file.read()

    # Initialize lexer, parser, and interpreter
    lexer = Lexer(text)
    parser = Parser(lexer)
    tree = parser.parse()
    interpreter = Interpreter()

    # Interpret the AST and print the result if there is one
    result = interpreter.interpret(tree)
    if result is not None:
        print(result)


if __name__ == '__main__':
    # If a file path is provided as a command-line argument, run the program from the file
    if len(sys.argv) == 2:
        run_program(sys.argv[1])
    else:
        # Otherwise, start the REPL for interactive use
        repl = REPL()
        repl.start()
