from lark import Lark, Transformer
import sys

# Load the grammar from grammarl.lark
with open("grammar.lark", "r") as grammar_file:
    grammar = grammar_file.read()

# Create a Lark parser
parser = Lark(grammar, parser='lalr')

# Define an AST transformer
class CalcTransformer(Transformer):
    def plus(self, items):
        return ('plus', items[0], items[1])
    
    def minus(self, items):
        return ('minus', items[0], items[1])
    
    def times(self, items):
        return ('times', items[0], items[1])
    
    def power(self, items):
        return ('power', items[0], items[1])
    
    def log_base(self, items):
        return ('log_base', items[0], items[1])

    def neg(self, items):
        return ('neg', items[0])
    
    def num(self, items):
        return ('num', int(items[0]))

# Function to evaluate the AST
def evaluate(ast):
    if ast[0] == 'plus':
        return evaluate(ast[1]) + evaluate(ast[2])
    elif ast[0] == 'minus':
        return evaluate(ast[1]) - evaluate(ast[2])
    elif ast[0] == 'times':
        return evaluate(ast[1]) * evaluate(ast[2])
    elif ast[0] == 'power':
        return evaluate(ast[1]) ** evaluate(ast[2])
    elif ast[0] == 'log_base':
        return log_base(evaluate(ast[1]), evaluate(ast[2]))
    elif ast[0] == 'neg':
        return -evaluate(ast[1])
    elif ast[0] == 'num':
        return ast[1]
    else:
        raise ValueError(f"Unknown operation: {ast}")

# Function to calculate logarithm with a specified base
def log_base(x, base, iterations=1000):
    if x <= 0 or base <= 0 or base == 1:
        raise ValueError("Logarithm only defined for positive numbers and base cannot be 1")
    n = iterations
    return int(n * ((x ** (1/n)) - 1) / (n * ((base ** (1/n)) - 1)))

# Main execution
if __name__ == "__main__":
    calc_transformer = CalcTransformer() 
    input_string = sys.argv[1]
    tree = parser.parse(input_string)  # Add this line
    #print(tree)
    ast = calc_transformer.transform(tree)
    #print(ast)
    result = evaluate(ast)
    print(result)