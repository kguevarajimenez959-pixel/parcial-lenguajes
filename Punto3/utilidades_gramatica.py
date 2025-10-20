from constantes import EPS


def parsear_gramatica(texto):
    """Parsea una gramática en formato textual y regresa (S, NT, T, R)."""
    lineas = []
    for cruda in texto.splitlines():
        s = cruda.strip()
        if not s or s.startswith("#"):
            continue
        lineas.append(s)
    reglas = {}
    NT = set()
    T = set()
    S = None
    for lin in lineas:
        if "->" not in lin:
            raise ValueError("Línea inválida: " + lin)
        izq, der = lin.split("->", 1)
        A = izq.strip()
        if S is None:
            S = A
        NT.add(A)
        variantes = [alt.strip() for alt in der.split("|")]
        for alt in variantes:
            if alt == "" or alt == EPS:
                cuerpo = (EPS,)
            else:
                cuerpo = tuple([x for x in alt.split(" ") if x != ""])
            reglas.setdefault(A, []).append(cuerpo)
    for A, cuerpos in reglas.items():
        for cuerpo in cuerpos:
            for X in cuerpo:
                if X not in NT and X != EPS:
                    T.add(X)
    return S, NT, T, reglas


def gramatica_ll1_estandar():
    """Regresa la gramática LL(1) fijada para las expresiones aritméticas."""
    NT = set(["E", "E'", "T", "T'", "F"])
    T = set(["+", "*", "(", " )".replace(" ", ""), "id"])
    T.discard(")")
    T.add(")")
    R = {
        "E": [("T", "E'")],
        "E'": [("+", "T", "E'"), (EPS,)],
        "T": [("F", "T'")],
        "T'": [("*", "F", "T'"), (EPS,)],
        "F": [("(", "E", ")"), ("id",)],
    }
    return "E", NT, T, R
