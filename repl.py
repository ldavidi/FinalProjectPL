from lexer import Lexer
from parser import Parser
from interpreter import Interpreter


class REPL:
    """Read-Eval-Print Loop (REPL) for the Functional Language Interpreter."""

    def __init__(self):
        self.lexer = None
        self.parser = None
        self.interpreter = Interpreter()

    def start(self):
        """Start the REPL session."""
        print("Welcome to the Functional Language Interpreter REPL. Type 'exit' to quit.")

        buffer = ""  # Accumulates lines for multi-line input
        while True:
            try:
                # Use '...' as a prompt when there's accumulated text, otherwise '>>>'
                prompt = '... ' if buffer else '>>> '
                line = input(prompt)

                # Exit the REPL on 'exit' command
                if line.strip().lower() == 'exit':
                    return

                buffer += line + "\n"  # Add the line to the buffer

                # Check if the input contains unbalanced braces
                open_braces = buffer.count('{')
                close_braces = buffer.count('}')

                # If braces are balanced, process the input
                if open_braces == close_braces:
                    self.lexer = Lexer(buffer.strip())
                    self.parser = Parser(self.lexer)
                    tree = self.parser.parse()
                    result = self.interpreter.interpret(tree)

                    # Print the result if it is not None
                    if result is not None:
                        print(result)

                    # Clear the buffer after processing
                    buffer = ""
            except Exception as error:
                print(f'Error: {error}')
                buffer = ""  # Clear the buffer in case of error

