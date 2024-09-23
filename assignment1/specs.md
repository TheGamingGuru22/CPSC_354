# John Mulhern rendition of Assignment 1

## Part 1: Parentheses Parser

### Description

The first part of the assignment requires implementing a function to check if a given string containing parentheses is balanced. A string is considered balanced if every opening parenthesis has a corresponding closing parenthesis and if no parenthesis is unpaired.

## Part 2: Calculator

### Description

The second part of the assignment requires implementing a calculator that can evaluate arithmetic expressions containing parentheses and the four basic operations (addition, subtraction, multiplication, division). The calculator should be able to handle both integer and floating-point numbers.

### Implementation

The calculator function uses two stacks: one for operators and one for values. It iterates through the input string, handling different characters appropriately:

- **Spaces**: Ignored.
- **Digits**: Parsed to form numbers.
- **Opening Parenthesis**: Pushed onto the operators stack.
- **Closing Parenthesis**: Triggers calculation of sub-expressions until an opening parenthesis is encountered.
- **Operators**: Handled according to precedence rules.

The function uses helper functions to determine operator precedence and to apply operators to the values stack.