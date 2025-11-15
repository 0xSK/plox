
def error(line: int | None, message: str) -> None:
    """Print an error message."""
    print(f"[line {line if line is not None else "<Unknown>"}] Error: {message}")
