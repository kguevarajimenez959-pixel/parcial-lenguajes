# Parser LL(1) por descenso recursivo
# Gramática:
#   E  -> T Ep
#   Ep -> + T Ep | ε
#   T  -> id

from typing import List

class Parser:
    def __init__(self, tokens: List[str]):
        self.toks = tokens + ["$"]
        self.i = 0

    def la(self) -> str:
        return self.toks[self.i]

    def eat(self, t: str):
        if self.la() == t:
            self.i += 1
        else:
            raise SyntaxError(f"esperaba {t}, obtuve {self.la()}")

    def T(self):
        if self.la() == "id":
            self.eat("id")
        else:
            raise SyntaxError("T -> id")

    def Ep(self):
        if self.la() == "+":
            self.eat("+")
            self.T()
            self.Ep()
        elif self.la() in {"$", "id"}:
            return
        else:
            raise SyntaxError("Ep")

    def E(self):
        self.T()
        self.Ep()

def parse(tokens: List[str]) -> bool:
    p = Parser(tokens)
    try:
        p.E()
        return p.la() == "$"
    except SyntaxError:
        return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Uso: python3 ll1.py \"id + id + id\"")
        raise SystemExit(1)
    toks = sys.argv[1].split()
    print("ACEPTA" if parse(toks) else "RECHAZA")
