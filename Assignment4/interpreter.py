from lark import Lark, Transformer
import sys
import os

# Load the grammar from grammar.lark
with open("grammar.lark", "r") as grammar_file:
    grammar = grammar_file.read()

# Create a Lark parser
parser = Lark(grammar, parser='lalr')

# Unified Transformer
class UnifiedTransformer(Transformer):
    def lam(self, args):
        name, body = args
        return ('lam', str(name), body)

    def plus(self, args):
        return ('plus', args[0], args[1])

    def minus(self, args):
        return ('minus', args[0], args[1])

    def times(self, args):
        return ('times', args[0], args[1])

    def divide(self, args):
        return ('divide', args[0], args[1])

    def power(self, args):
        return ('power', args[0], args[1])

    def log_base(self, args):
        return ('log_base', args[0], args[1])

    def neg(self, args):
        return ('neg', args[0])

    def app(self, args):
        # Handle multiple applications
        if len(args) == 2:
            return ('app', args[0], args[1])
        else:
            func = args[0]
            for arg in args[1:]:
                func = ('app', func, arg)
            return func

    def num(self, args):
        return ('num', float(args[0]))

    def var(self, args):
        token, = args
        return ('var', str(token))

# Evaluate function
def evaluate(ast, env=None):
    if env is None:
        env = {}
    
    if isinstance(ast, (int, float)):
        return ast
    elif ast[0] == 'num':
        return ast[1]
    elif ast[0] == 'var':
        name = ast[1]
        if name in env:
            return env[name]
        else:
            raise Exception(f"Undefined variable: {name}")
    elif ast[0] == 'lam':
        return ('closure', ast[1], ast[2], env.copy())
    elif ast[0] == 'app':
        func = evaluate(ast[1], env)
        arg = evaluate(ast[2], env)
        if func[0] == 'closure':
            param, body, closure_env = func[1], func[2], func[3]
            closure_env[param] = arg
            return evaluate(body, closure_env)
        else:
            raise Exception(f"Cannot apply non-function: {func}")
    elif ast[0] == 'plus':
        return evaluate(ast[1], env) + evaluate(ast[2], env)
    elif ast[0] == 'minus':
        return evaluate(ast[1], env) - evaluate(ast[2], env)
    elif ast[0] == 'times':
        return evaluate(ast[1], env) * evaluate(ast[2], env)
    elif ast[0] == 'divide':
        denominator = evaluate(ast[2], env)
        if denominator == 0:
            raise ZeroDivisionError("Division by zero")
        return evaluate(ast[1], env) / denominator
    elif ast[0] == 'power':
        return evaluate(ast[1], env) ** evaluate(ast[2], env)
    elif ast[0] == 'log_base':
        import math
        base = evaluate(ast[2], env)
        value = evaluate(ast[1], env)
        if base <= 0 or base == 1:
            raise ValueError("Invalid base for logarithm")
        if value <= 0:
            raise ValueError("Logarithm only defined for positive numbers")
        return math.log(value, base)
    elif ast[0] == 'neg':
        return -evaluate(ast[1], env)
    else:
        raise Exception(f"Unknown AST node: {ast}")

# Custom Transformation Function
def custom_transform(ast):
    if isinstance(ast, (int, float)):
        return str(ast)
    elif ast[0] == 'num':
        return str(ast[1])
    elif ast[0] == 'var':
        return ast[1]
    elif ast[0] == 'lam':
        return f"(\\{ast[1]}.{custom_transform(ast[2])})"
    elif ast[0] == 'app':
        func = custom_transform(ast[1])
        arg = custom_transform(ast[2])
        return f"({func} {arg})"
    elif ast[0] == 'plus':
        left = custom_transform(ast[1])
        right = custom_transform(ast[2])
        return f"({left} + {right})"
    elif ast[0] == 'minus':
        left = custom_transform(ast[1])
        right = custom_transform(ast[2])
        # Apply specific transformation for double negatives
        if right.startswith('-'):
            # Change 'left - -right' to 'left + right'
            right = right.lstrip('-')
            return f"({left} + {right})"
        else:
            return f"({left} - {right})"
    elif ast[0] == 'times':
        left = custom_transform(ast[1])
        right = custom_transform(ast[2])
        # If both left and right are negative numbers, multiply and make positive
        if left.startswith('-') and right.startswith('-'):
            left_num = float(left)
            right_num = float(right)
            product = left_num * right_num
            return str(product)
        else:
            return f"({left} * {right})"
    elif ast[0] == 'divide':
        left = custom_transform(ast[1])
        right = custom_transform(ast[2])
        return f"({left} / {right})"
    elif ast[0] == 'power':
        base = custom_transform(ast[1])
        exponent = custom_transform(ast[2])
        return f"({base} ^ {exponent})"
    elif ast[0] == 'log_base':
        value = custom_transform(ast[1])
        base = custom_transform(ast[2])
        return f"(log({value}) base({base}))"
    elif ast[0] == 'neg':
        expr = custom_transform(ast[1])
        # Simplify multiple negations
        if expr.startswith('-'):
            # '--expr' becomes 'expr'
            return expr[1:]
        else:
            return f"-{expr}"
    else:
        raise Exception(f"Unknown AST node: {ast}")

# Main execution
def main():
    if len(sys.argv) != 2:
        print("Usage: python interpreter.py '<expression>'", file=sys.stderr)
        sys.exit(1)

    input_arg = sys.argv[1]

    if os.path.isfile(input_arg):
        # If the input is a valid file path, read from the file
        with open(input_arg, 'r') as file:
            expression = file.read()
    else:
        # Otherwise, treat the input as a direct expression
        expression = input_arg
    try:
        # Parse the expression
        tree = parser.parse(expression)

        # Transform the parse tree into an AST
        transformer = UnifiedTransformer()
        ast = transformer.transform(tree)

        # Try to evaluate the AST
        result = evaluate(ast)
        print(f"{result}")
    except Exception as e:
        # If evaluation fails, output the transformed expression
        transformed_expr = custom_transform(ast)
        print(f"{transformed_expr}")

if __name__ == "__main__":
    main()
