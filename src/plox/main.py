"""
Main entry point for the Plox interpreter.
"""

import sys
from pathlib import Path


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
    print(f"Source code:\n{source}")


def run_prompt() -> None:
    """Run the interactive REPL."""
    print("Plox interpreter v0.1.0")
    print("Type 'exit' or 'quit' to exit")
    print()
    
    while True:
        try:
            line = input("plox> ")
            if line.lower() in ('exit', 'quit'):
                break
            
            # TODO: Implement interpreter
            print(f"Input: {line}")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()

