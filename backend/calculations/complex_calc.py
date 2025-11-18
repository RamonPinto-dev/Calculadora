import ast
import re

def normalize_complex(expr):
    return re.sub(r'(?<![\w])j', '1j', expr)

class verify_entry(ast.NodeVisitor):
    
        allowed_nodes = (
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Constant,

        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow,
        ast.UAdd, ast.USub,)
                               
        
        def visit(self, node):
            if not isinstance(node, self.allowed_nodes):
                raise ValueError(f"Expressão proibida: {ast.dump(node)}")
            return super().visit(node)
        


def complex_calc(expression):       
    
    expression = normalize_complex(expression)
    tree = ast.parse(expression, mode="eval")

    verify_entry().visit(tree)

    return eval(
        expression,
        {"__builtins__": None},
        {
           
            "j": 1j,
            "complex": complex
        }
    )