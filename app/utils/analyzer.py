import ast

def analyze_python_code(code_text: str):
    """
    Analiza código fuente de Python sin ejecutarlo.
    Cuenta clases, funciones y detecta docstrings.
    """
    try:
        tree = ast.parse(code_text)
        
        stats = {
            "num_classes": 0,
            "num_functions": 0,
            "has_docstrings": False
        }

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                stats["num_classes"] += 1
            elif isinstance(node, ast.FunctionDef):
                stats["num_functions"] += 1
            
            # Verificar si hay comentarios de documentación
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
                if ast.get_docstring(node):
                    stats["has_docstrings"] = True

        return stats
    except SyntaxError:
        return {"error": "No se pudo parsear el archivo (posible error de sintaxis o no es Python)"}