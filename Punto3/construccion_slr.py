from constantes import EOF
from first_follow_predict import primeros, siguientes


def _cierre(I, NT, T, R):  # noqa: E741
    C = set(I)
    cambio = True
    while cambio:
        cambio = False
        nuevos = set()
        for A, alfa, p in list(C):
            X = alfa[p] if p < len(alfa) else None
            if X in NT:
                for cuerpo in R[X]:
                    cand = (X, cuerpo, 0)
                    if cand not in C:
                        nuevos.add(cand)
        if nuevos:
            C |= nuevos
            cambio = True
    return C


def _ir_a(I, X, NT, T, R):  # noqa: E741
    J = set()
    for A, alfa, p in I:
        if p < len(alfa) and alfa[p] == X:
            J.add((A, alfa, p + 1))
    if not J:
        return set()
    return _cierre(J, NT, T, R)


def _coleccion_canonica(S, NT, T, R):
    Sprima = "S'"
    NT_aug = set(NT)
    NT_aug.add(Sprima)
    R_aug = {k: list(v) for k, v in R.items()}
    R_aug[Sprima] = [(S,)]
    T_aug = set(T)
    I0 = _cierre(set([(Sprima, (S,), 0)]), NT_aug, T_aug, R_aug)

    estados = [frozenset(I0)]
    trans = [dict()]
    mapa = {estados[0]: 0}
    pila = [I0]

    while pila:
        I = pila.pop()  # noqa: E741
        i = mapa[frozenset(I)]
        simbolos = set(NT_aug) | set(T_aug)
        for X in simbolos:
            J = _ir_a(I, X, NT_aug, T_aug, R_aug)
            if not J:
                continue
            fJ = frozenset(J)
            if fJ not in mapa:
                mapa[fJ] = len(estados)
                estados.append(fJ)
                trans.append({})
                pila.append(J)
            trans[i][X] = mapa[fJ]
    return [set(S) for S in estados], trans, Sprima, NT_aug, T_aug, R_aug


def tabla_slr(S, NT, T, R):
    """Construye las tablas ACTION y GOTO de un parser SLR(1)."""
    C, trans, Sprima, NTa, Ta, Ra = _coleccion_canonica(S, NT, T, R)

    first_aug = primeros(Sprima, NTa, Ta, Ra)
    follow_aug = siguientes(Sprima, NTa, Ta, Ra, first_aug)

    action = []
    goto = {}
    n = len(C)
    for i in range(n):
        action.append({})
        goto[i] = {}

    for i in range(n):
        for a in trans[i]:
            if a in Ta:
                action[i][a] = ("s", trans[i][a], None)
            else:
                goto[i][a] = trans[i][a]
        I = C[i]  # noqa: E741
        for A, alfa, p in I:
            if p == len(alfa):
                if A == Sprima:
                    action[i][EOF] = ("acc", None, None)
                else:
                    for a in follow_aug[A]:
                        if a in action[i] and action[i][a][0] == "s":
                            continue
                        action[i][a] = ("r", None, (A, alfa))
    return action, goto
