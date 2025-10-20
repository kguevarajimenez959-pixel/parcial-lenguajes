from constantes import EPS, EOF
from utilidades_gramatica import gramatica_ll1_estandar


def escanear(cadena):
    """Tokeniza la cadena de entrada en pares (tipo, lexema)."""
    toks = []
    i = 0
    while i < len(cadena):
        c = cadena[i]
        if c.isspace():
            i += 1
            continue
        if c.isalpha() or c == "_":
            j = i + 1
            while j < len(cadena) and (cadena[j].isalnum() or cadena[j] == "_"):
                j += 1
            toks.append(("id", cadena[i:j]))
            i = j
            continue
        if c in "+*()":
            toks.append((c, c))
            i += 1
            continue
        raise ValueError("Carácter inválido: " + c)
    toks.append((EOF, EOF))
    return toks


def parse_slr(toks, action, goto):
    """Ejecuta el parser SLR(1) usando las tablas ACTION y GOTO."""
    estados = [0]
    pila = []
    k = 0
    while True:
        s = estados[-1]
        a = toks[k][0]
        act = action[s].get(a)
        if act is None:
            return False
        t = act[0]
        if t == "s":
            pila.append(a)
            estados.append(act[1])
            k += 1
        elif t == "r":
            (A, alfa) = act[2]
            n = len(alfa)
            if alfa != (EPS,):
                for _ in range(n):
                    pila.pop()
                    estados.pop()
            pila.append(A)
            ns = goto[estados[-1]].get(A)
            if ns is None:
                return False
            estados.append(ns)
        else:
            return True


def _tokenizar_ll1(cadena):
    toks = []
    i = 0
    while i < len(cadena):
        c = cadena[i]
        if c.isspace():
            i += 1
            continue
        if c.isalpha() or c == "_":
            j = i + 1
            while j < len(cadena) and (cadena[j].isalnum() or cadena[j] == "_"):
                j += 1
            toks.append("id")
            i = j
            continue
        if c in "+*()":
            toks.append(c)
            i += 1
            continue
        raise ValueError("Carácter inválido: " + c)
    toks.append(EOF)
    return toks


def traza_ll1(expresion):
    """Genera los pasos de un parser predictivo LL(1)."""
    S, NT, T, R = gramatica_ll1_estandar()
    toks = _tokenizar_ll1(expresion)
    k = 0
    a = toks[k]
    pila = ["E"]
    pasos = []

    while pila:
        X = pila.pop()
        if X in T or X == EOF or X == "id" or X in ["+", "*", "(", ")"]:
            if X == a or (X == "id" and a == "id"):
                pasos.append(" - Consumir " + a)
                k += 1
                a = toks[k]
            else:
                pasos.append(" - Error")
                break
        elif X == "E":
            pasos.append(" - E → T E'")
            pila.append("E'")
            pila.append("T")
        elif X == "E'":
            if a == "+":
                pasos.append(" - E' → + T E'")
                pila.append("E'")
                pila.append("T")
                pila.append("+")
            else:
                pasos.append(" - E' → ε")
        elif X == "T":
            pasos.append(" - T → F T'")
            pila.append("T'")
            pila.append("F")
        elif X == "T'":
            if a == "*":
                pasos.append(" - T' → * F T'")
                pila.append("T'")
                pila.append("F")
                pila.append("*")
            else:
                pasos.append(" - T' → ε")
        elif X == "F":
            if a == "(":
                pasos.append(" - F → ( E )")
                pila.append(")")
                pila.append("E")
                pila.append("(")
            elif a == "id":
                pasos.append(" - F → id")
                pila.append("id")
            else:
                pasos.append(" - Error")
                break
        else:
            pasos.append(" - Error")
            break

    if a == EOF and " - Error" not in pasos:
        pasos.append(" - Aceptar")
    return pasos


def traza_ll1_info(expresion):
    """Versión extendida de traza_ll1 con información de producciones usadas."""
    S, NT, T, R = gramatica_ll1_estandar()
    toks = _tokenizar_ll1(expresion)
    k = 0
    a = toks[k]
    pila = ["E"]
    pasos = []
    nts_usados = set()
    prods_usadas = []

    while pila:
        X = pila.pop()
        if X in T or X == EOF or X == "id" or X in ["+", "*", "(", ")"]:
            if X == a or (X == "id" and a == "id"):
                pasos.append(" - Consumir " + a)
                k += 1
                a = toks[k]
            else:
                pasos.append(" - Error")
                break
        elif X == "E":
            pasos.append(" - E → T E'")
            nts_usados.add("E")
            prods_usadas.append(("E", ("T", "E'")))
            pila.append("E'")
            pila.append("T")
        elif X == "E'":
            nts_usados.add("E'")
            if a == "+":
                pasos.append(" - E' → + T E'")
                prods_usadas.append(("E'", ("+", "T", "E'")))
                pila.append("E'")
                pila.append("T")
                pila.append("+")
            else:
                pasos.append(" - E' → ε")
                prods_usadas.append(("E'", (EPS,)))
        elif X == "T":
            pasos.append(" - T → F T'")
            nts_usados.add("T")
            prods_usadas.append(("T", ("F", "T'")))
            pila.append("T'")
            pila.append("F")
        elif X == "T'":
            nts_usados.add("T'")
            if a == "*":
                pasos.append(" - T' → * F T'")
                prods_usadas.append(("T'", ("*", "F", "T'")))
                pila.append("T'")
                pila.append("F")
                pila.append("*")
            else:
                pasos.append(" - T' → ε")
                prods_usadas.append(("T'", (EPS,)))
        elif X == "F":
            nts_usados.add("F")
            if a == "(":
                pasos.append(" - F → ( E )")
                prods_usadas.append(("F", ("(", "E", ")")))
                pila.append(")")
                pila.append("E")
                pila.append("(")
            elif a == "id":
                pasos.append(" - F → id")
                prods_usadas.append(("F", ("id",)))
                pila.append("id")
            else:
                pasos.append(" - Error")
                break
        else:
            pasos.append(" - Error")
            break

    if a == EOF and " - Error" not in pasos:
        pasos.append(" - Aceptar")
    return pasos, nts_usados, prods_usadas
