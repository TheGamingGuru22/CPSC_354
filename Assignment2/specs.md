# John Mulhern rendition of Assignment 2

## Project Overview

This project is a simple calculator that can evaluate arithmetic expressions. It uses the Lark library to parse the provided input string from the command line and then transforms the parse tree into an Abstract Syntax Tree (AST). The AST is then evaluated using the evaluate function and the result is printed to the console.

## Part 1: Grammar.Lark File

### Description

The Grammar.Lark file defines the grammar for a simple arithmetic expression language. It includes rules for handling numbers, parentheses, and the four basic arithmetic operations (addition, subtraction, multiplication, division), as well as the unary minus operation, logarithmic expressions, and exponentiation.

## Part 2: calculator_cfg.py

### Description

The calculator_cfg.py file is a Python script that defines a calculator for arithmetic expressions. It uses the Lark library as well as the grammar.lark file to parse the input string and then transforms the parse tree into an Abstract Syntax Tree (AST). The AST is then evaluated using the evaluate function.

### Method Definitions

#### Calculator Transformer

The Calculator Transformer class is a subclass of the Lark Transformer class. It defines methods for each non-terminal symbol in the grammar. Each method takes a list of parsed tokens and returns an AST node.

#### evaluate

The evaluate method is a recursive method that evaluates the AST. It takes an AST node and returns a value. The evaluate method handles the four basic arithmetic operations (addition, subtraction, multiplication, division) and the unary minus operation. 

#### log_base

The log_base method is a helper method that calculates the logarithm of a number with a specified base. It takes two numbers and an optional number of iterations (default is 1000). It uses the formula for the nth root of a number to calculate the logarithm. 

#### Main Execution

The main execution of the calculator_cfg.py file takes in a command line argument for the arithmetic expression and prints the result to the console.
