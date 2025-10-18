# src/parser.py
from dataclasses import dataclass
from typing import List, Union
from .lexer import lex, Token

@dataclass
class Num:  value: float
@dataclass
class Bin:  op: str; left: "Node"; right: "Node"
Node = Union[Num, Bin]

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.i = 0  # índice del lookahead

    # === Algoritmo de emparejamiento (match) ===
    def match(self, *expected_types: str) -> bool:
        """Si el token actual pertenece a expected_types, lo consume y retorna True.
        Si no, no avanza y retorna False."""
        if self.peek().type in expected_types:
            self.i += 1
            return True
        return False

    def consume(self, expected_type: str, msg: str):
        """Empareja o lanza error claro."""
        if self.match(expected_type):
            return self.tokens[self.i - 1]
        t = self.peek()
        raise SyntaxError(f"{msg}. Encontrado {t.type} '{t.lexeme}' en pos {t.pos}")

    def peek(self) -> Token:
        return self.tokens[self.i]

    # Gramática:
    # E -> T ((PLUS|MINUS) T)*
    # T -> F ((MUL|DIV) F)*
    # F -> NUM | LP E RP
    def parse(self) -> Node:
        node = self.E()
        self.consume("EOF", "Se esperaba fin de entrada")
        return node

    def E(self) -> Node:
        node = self.T()
        while self.match("PLUS", "MINUS"):
            op = self.tokens[self.i - 1].type
            right = self.T()
            node = Bin(op, node, right)
        return node

    def T(self) -> Node:
        node = self.F()
        while self.match("MUL", "DIV"):
            op = self.tokens[self.i - 1].type
            right = self.F()
            node = Bin(op, node, right)
        return node

    def F(self) -> Node:
        if self.match("NUM"):
            tok = self.tokens[self.i - 1]
            return Num(float(tok.lexeme))
        if self.match("LP"):
            node = self.E()
            self.consume("RP", "Falta ')'")
            return node
        t = self.peek()
        raise SyntaxError(f"Expresión inválida en pos {t.pos}")

# Evaluador opcional para verificar el AST
def eval_ast(n: Node) -> float:
    if isinstance(n, Num):
        return n.value
    l, r = eval_ast(n.left), eval_ast(n.right)
    if n.op == "PLUS":  return l + r
    if n.op == "MINUS": return l - r
    if n.op == "MUL":   return l * r
    if n.op == "DIV":   return l / r
    raise ValueError("Operador desconocido")
