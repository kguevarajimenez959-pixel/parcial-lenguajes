# CYK con cierres unitarios para lenguaje: id (+ id)*
# Gramática equivalente sin ε explícita:
#   Term: ID->id, PLUS->+
#   Unit: T->ID, E->T, X->T
#   Bin : E->T Ep, Ep->PLUS X, X->T Ep

from typing import List, Set, Dict, Tuple

# Binarias A -> B C
BIN: Dict[str, Set[Tuple[str,str]]] = {
    "E": {("T","Ep")},
    "Ep": {("PLUS","X")},
    "X": {("T","Ep")},
}

# Preterminales A -> a
PRE: Dict[str, str] = {
    "ID": "id",
    "PLUS": "+",
}

# ID -> T ; T -> E, X
UNIT_UP: Dict[str, Set[str]] = {
    "ID": {"T"},
    "T": {"E", "X"},
    # No hay cierres desde PLUS
}

START = "E"

def unit_closure(symbols: Set[str]) -> Set[str]:
    """Añade ancestros por reglas unitarias hasta cierre."""
    changed = True
    out = set(symbols)
    while changed:
        changed = False
        for s in list(out):
            for parent in UNIT_UP.get(s, ()):
                if parent not in out:
                    out.add(parent)
                    changed = True
    return out

def cyk_parse(tokens: List[str]) -> bool:
    n = len(tokens)
    if n == 0:
        return False

    # table[i][l] = conjunto para subcadena tokens[i:i+l]
    table: List[List[Set[str]]] = [[set() for _ in range(n+1)] for _ in range(n)]

    # Longitud 1
    for i, tok in enumerate(tokens):
        cell = set()
        for A, a in PRE.items():
            if tok == a:
                cell.add(A)
        cell = unit_closure(cell)
        table[i][1] = cell

    # Longitudes >=2
    for l in range(2, n+1):
        for i in range(0, n - l + 1):
            cell = set()
            for split in range(1, l):
                L = table[i][split]
                R = table[i+split][l - split]
                if not L or not R:
                    continue
                for A, pairs in BIN.items():
                    for (B, C) in pairs:
                        if B in L and C in R:
                            cell.add(A)
            # cierre unitario después de combinaciones
            table[i][l] = unit_closure(cell)

    return START in table[0][n]

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print('Uso: python3 cyk.py "id + id + id"')
        raise SystemExit(1)
    toks = sys.argv[1].split()
    print("ACEPTA" if cyk_parse(toks) else "RECHAZA")

