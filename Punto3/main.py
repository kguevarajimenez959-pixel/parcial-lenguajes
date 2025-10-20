import funciones


def leer_txt(ruta):
    f = open(ruta, "r", encoding="utf-8")
    try:
        return f.read()
    finally:
        f.close()


def cargar_original():
    txt = leer_txt("gramatica.txt")
    S, NT, T, R = funciones.parsear_gramatica(txt)
    return S, NT, T, R


def imprimir_gramaticas():
    S, NT, T, R = cargar_original()
    print("== Gramática original ==")
    ks = []
    for A in R:
        ks.append(A)
    ks.sort()
    for A in ks:
        for alfa in R[A]:
            print(" ", A, "→", " ".join(alfa))

    S1, NT1, T1, R1 = funciones.gramatica_ll1_estandar()
    print("== Gramática LL(1) ==")
    orden = ["E", "E'", "T", "T'", "F"]
    usados = {}
    for A in orden:
        usados[A] = True
        if A in R1:
            for alfa in R1[A]:
                print(" ", A, "→", " ".join(alfa))
    for A in R1:
        if A not in usados:
            for alfa in R1[A]:
                print(" ", A, "→", " ".join(alfa))


def imprimir_conjuntos_filtrados(nts_usados, prods_usadas):
    # Calcular FIRST/FOLLOW/PREDICT en la LL(1) y filtrar por lo que se usó
    S1, NT1, T1, R1 = funciones.gramatica_ll1_estandar()
    FIRST = funciones.primeros(S1, NT1, T1, R1)
    FOLLOW = funciones.siguientes(S1, NT1, T1, R1, FIRST)
    PRED = funciones.prediccion(NT1, R1, FIRST, FOLLOW)

    def _fmt_set(s):
        v = list(s)
        v.sort()  # noqa: E702
        return "{ " + ", ".join(v) + " }"

    print("CONJUNTOS FIRST")
    print("----------------")
    orden = ["E", "E'", "T", "T'", "F"]
    # Mostrar solo los NT que aparecieron
    usados_orden = [x for x in orden if x in nts_usados]
    otros = []
    for A in nts_usados:
        if A not in usados_orden:
            otros.append(A)
    for A in usados_orden:
        print("FIRST(" + A + ") =", _fmt_set(FIRST[A]))
    for A in sorted(otros):
        print("FIRST(" + A + ") =", _fmt_set(FIRST[A]))

    print("")
    print("CONJUNTOS FOLLOW")
    print("-----------------")
    for A in usados_orden:
        print("FOLLOW(" + A + ") =", _fmt_set(FOLLOW[A]))
    for A in sorted(otros):
        print("FOLLOW(" + A + ") =", _fmt_set(FOLLOW[A]))

    print("")
    print("PREDICT")
    print("-------")
    # Mostrar solo producciones usadas
    # Mantener el orden de aparición
    vistos = set()
    for A, alfa in prods_usadas:
        key = (A, alfa)
        if key in vistos:
            continue
        vistos.add(key)
        conj = PRED[key]
        print(A, "→", " ".join(alfa) + ":", _fmt_set(conj))
    print("")


def _obtener_argumentos():
    try:
        with open("/proc/self/cmdline", "rb") as f:
            partes = f.read().split(b"\0")
    except OSError:
        return []
    decodificados = []
    for item in partes:
        if not item:
            continue
        try:
            decodificados.append(item.decode("utf-8"))
        except UnicodeDecodeError:
            decodificados.append(item.decode("latin1"))
    if not decodificados:
        return []
    argumentos = decodificados[1:]
    if not argumentos:
        return []
    script = __file__
    nombre = script.rsplit("/", 1)[-1]
    candidato = argumentos[0]
    if (
        candidato == script
        or candidato == nombre
        or candidato.endswith("/" + nombre)
    ):
        argumentos = argumentos[1:]
    args = []
    for elemento in argumentos:
        if elemento:
            args.append(elemento)
    return args


def _leer_desde_stdin():
    try:
        flujo = open("/dev/stdin", "r", encoding="utf-8")
    except OSError:
        return []
    try:
        if flujo.isatty():
            return []
        data = flujo.read()
    finally:
        flujo.close()
    entradas = []
    for linea in data.splitlines():
        linea = linea.strip()
        if linea:
            entradas.append(linea)
    return entradas


def _leer_interactivo():
    entradas = []
    try:
        while True:
            linea = input("> ").strip()
            if linea:
                entradas.append(linea)
    except EOFError:
        pass
    return entradas


def main():
    args = _obtener_argumentos()

    if len(args) == 1 and args[0] == "--info":
        imprimir_gramaticas()
        return

    entradas = list(args)
    if not entradas:
        entradas = _leer_desde_stdin()
    if not entradas:
        entradas = _leer_interactivo()

    # Trazas y recolección de símbolos usados
    nts_total = set()
    prods_total = []
    for expr in entradas:
        print("Expresión:", expr)
        print("Pasos del parser:")
        pasos, nts_usados, prods_usadas = funciones.traza_ll1_info(expr)
        for p in pasos:
            print(p)
        print("")
        nts_total |= nts_usados
        prods_total += prods_usadas

    # Conjuntos solo de lo usado
    if entradas:
        imprimir_conjuntos_filtrados(nts_total, prods_total)


main()
