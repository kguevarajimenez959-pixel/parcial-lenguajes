# Punto 4 – Comparación de rendimiento: CYK vs LL(1)

Lenguaje de prueba: cadenas del tipo `id (+ id)*` con tokens separados por espacios.

## Gramáticas

### LL(1)
```text
E  -> T Ep
Ep -> + T Ep | ε
T  -> id
