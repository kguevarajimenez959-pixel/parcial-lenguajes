# src/main.py
from .lexer import lex
from .parser import Parser, eval_ast

def run(src: str):
    tokens = list(lex(src))
    ast = Parser(tokens).parse()
    return ast, eval_ast(ast)

if __name__ == "__main__":
    while True:
        try:
            line = input("> ")
            if not line: continue
            ast, val = run(line)
            print("OK =", val)
        except EOFError:
            break
        except Exception as e:
            print("Error:", e)
