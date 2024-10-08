import sys

def balance_check(expression):
    stack = []
    for char in expression:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if not stack:
                return False
            stack.pop()
    return not stack

expression = sys.argv[1]

if balance_check(expression) == True:
    print("yes")
else:
    print("no")
