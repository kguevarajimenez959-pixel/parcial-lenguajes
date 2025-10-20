from constantes import EPS, EOF


def primeros(S, NT, T, R):
    """Calcula FIRST para todos los símbolos."""
    first = {}
    for X in NT:
        first[X] = set()
    for x in T:
        first[x] = set([x])
    first[EPS] = set([EPS])

    cambio = True
    while cambio:
        cambio = False
        for A in NT:
            for beta in R[A]:
                vacio = True
                for X in beta:
                    antes = len(first[A])
                    first[A] |= first[X] - set([EPS])
                    if EPS not in first[X]:
                        vacio = False
                        break
                    if len(first[A]) > antes:
                        cambio = True
                if vacio:
                    if EPS not in first[A]:
                        first[A].add(EPS)
                        cambio = True
    return first


def _first_de_secuencia(seq, first):
    s = set()
    eps = True
    for X in seq:
        s |= first[X] - set([EPS])
        if EPS not in first[X]:
            eps = False
            break
    if eps:
        s.add(EPS)
    return s


def siguientes(S, NT, T, R, first):
    """Calcula FOLLOW para los no terminales."""
    follow = {}
    for A in NT:
        follow[A] = set()
    follow[S].add(EOF)

    cambio = True
    while cambio:
        cambio = False
        for A in NT:
            for beta in R[A]:
                n = len(beta)
                for i in range(n):
                    B = beta[i]
                    if B in NT:
                        cola = beta[i + 1 :]
                        fs = _first_de_secuencia(cola, first)
                        antes = len(follow[B])
                        follow[B] |= fs - set([EPS])
                        if EPS in fs:
                            follow[B] |= follow[A]
                        if len(follow[B]) > antes:
                            cambio = True
    return follow


def prediccion(NT, R, first, follow):
    """Construye los conjuntos PREDICT para cada producción."""
    predict = {}
    for A in NT:
        for alfa in R[A]:
            key = (A, alfa)
            if alfa == (EPS,):
                predict[key] = set(follow[A])
            else:
                s = set()
                eps = True
                for X in alfa:
                    s |= first[X] - set([EPS])
                    if EPS not in first[X]:
                        eps = False
                        break
                if eps:
                    s |= follow[A]
                predict[key] = s
    return predict
