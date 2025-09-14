# Plox

A Python interpreter for the Lox programming language.

## Overview

This is a hobby project implementing an interpreter for the Lox programming language in Python, 
following the book "Crafting Interpreters" by Robert Nystrom. Lox is a simple, dynamically-typed 
programming language designed for learning about language implementation.

## Features

TBD

## Installation

This project uses `uv` for dependency management. Make sure you have `uv` installed:

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then install the project:

```bash
# Install dependencies
uv sync

# Install the package in development mode
uv pip install -e .
```

## Usage

```bash
# Run the REPL
uv run plox

# Run a Lox script
uv run plox script.lox
```
