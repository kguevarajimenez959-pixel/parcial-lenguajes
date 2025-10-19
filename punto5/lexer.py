# src/lexer.py
import re
from dataclasses import dataclass

@dataclass
class Token:
    type: str
    lexeme: str
    pos: int

TOKEN_SPEC = [
    ("NUM",   r"\d+(\.\d+)?"),
    ("PLUS",  r"\+"),
    ("MINUS", r"-"),
    ("MUL",   r"\*"),
    ("DIV",   r"/"),
    ("LP",    r"\("),
    ("RP",    r"\)"),
    ("WS",    r"[ \t\n]+"),
]

MASTER = re.compile("|".join(f"(?P<{t}>{p})" for t, p in TOKEN_SPEC))

def lex(source: str):
    pos = 0
    for m in MASTER.finditer(source):
        kind = m.lastgroup
        lexeme = m.group()
        if kind != "WS":
            yield Token(kind, lexeme, m.start())
        pos = m.end()
    if pos != len(source):
        raise SyntaxError(f"Carácter inválido en {pos}: {source[pos]!r}")
    yield Token("EOF", "", pos)
