import sys

# Helper function for performing operations
def apply_operator(operators, values):
    operator = operators.pop()
    right = values.pop()
    left = values.pop()
    
    if operator == '+':
        values.append(left + right)
    elif operator == '-':
        values.append(left - right)
    elif operator == '*':
        values.append(left * right)
    elif operator == '/':
        values.append(left / right)
    elif operator == '^':
        values.append(left ** right)

# Function to handle operator precedence
def precedence(op):
    if op in ('+', '-'):
        return 1
    if op in ('*', '/'):
        return 2
    if op in ('^'):
        return 3
    return 0

# Function to parse a number from the input string
def get_number(expression, i):
    num = 0
    while i < len(expression) and expression[i].isdigit():
        num = num * 10 + int(expression[i])
        i += 1
    return num, i

# Main calculator function that respects order of operations
def calculator(expression):
    # Stack to store operators and values
    values = []
    operators = []

    i = 0
    while i < len(expression):
        # If current char is a space, skip it
        if expression[i] == ' ':
            i += 1
            continue
        
        # If current char is a digit, parse the full number
        if expression[i].isdigit():
            num, i = get_number(expression, i)
            values.append(num)
        
        # If current char is an opening parenthesis
        elif expression[i] == '(':
            operators.append(expression[i])
            i += 1
        
        # If current char is a closing parenthesis, solve the sub-expression
        elif expression[i] == ')':
            while operators and operators[-1] != '(':
                apply_operator(operators, values)
            operators.pop()  # Pop the '('
            i += 1
        
        # If current char is an operator
        else:
            while (operators and operators[-1] != '(' and precedence(operators[-1]) >= precedence(expression[i])):
                apply_operator(operators, values)
            operators.append(expression[i])
            i += 1

    # Apply the remaining operators
    while operators:
        apply_operator(operators, values)

    # The final result will be the last value in the stack
    return values[0]

# Example usage
expression = sys.argv[1]
print(f"Result: {calculator(expression)}")