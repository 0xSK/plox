"""
Main entry point for the Plox interpreter.
"""

import sys
from pathlib import Path
from plox.scanner import Scanner
from plox.parser import Parser
from plox.interpreter import Interpreter
from plox.expression import AstPrinter

had_error: bool = False

def main() -> None:
    """Main entry point for the Plox interpreter."""
    if len(sys.argv) > 2:
        print("Usage: plox [script]")
        sys.exit(64)
    elif len(sys.argv) == 2:
        # Run script file
        run_file(sys.argv[1])
    else:
        # Run REPL
        run_prompt()

    if had_error:
        sys.exit(65)

def run_file(path: str) -> None:
    """Run a Lox script from a file."""
    try:
        with open(path, 'r', encoding='utf-8') as file:
            source = file.read()
    except FileNotFoundError:
        print(f"Error: Could not find file '{path}'")
        sys.exit(66)
    except IOError as e:
        print(f"Error reading file '{path}': {e}")
        sys.exit(66)
    
    # TODO: Implement interpreter
    print(f"Running file: {path}")
    run(source)

def run_prompt() -> None:
    """Run the interactive REPL."""
    print("Type 'exit' or 'quit' to exit")
    print()
    
    while True:
        try:
            line = input("plox> ")
            if line.lower() in ('exit', 'quit'):
                print("Goodbye!")
                break
            
            # TODO: Implement interpreter
            run(line)
            had_error = False
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break

def run(source: str) -> None:
    """Run the source code."""

    scanner = Scanner(source)
    # for now, just print the source and parsed tokens
    expr = Parser(scanner.tokens).parse()
    
    if expr is None:
        had_error = True
        print("Error was had in parsing.")
        return
    
    Interpreter().interpret(expr)
    
    # print(AstPrinter().pformat(expr))
    

def error(line: int, message: str) -> None:
    """Print an error message."""
    print(f"[line {line}] Error: {message}")


if __name__ == "__main__":
    main()

