# PARCIAL LENGUAJES

## Punto 4

# Proyecto Punto 4 – Comparación de rendimiento: CYK vs LL(1)

Este proyecto implementa dos analizadores sintácticos en Python para el mismo lenguaje, uno con el algoritmo **CYK** (O(n³)) y otro con **LL(1)** (O(n)), y compara su rendimiento mediante mediciones de tiempo.


## Instalación

### 1. Crear carpeta del proyecto

```
mkdir punto4
cd punto4
```

### 2. Crear los archivos del proyecto

#### 2.1 Archivo `cyk.py`

```
nano cyk.py
```

#### 2.2 Archivo `ll1.py`

```
nano ll1.py
```

#### 2.3 Archivo `bench.py`

```
nano bench.py
```

#### 2.4 Archivo `README.md`

```
nano README.md
```

## Uso

### Ejecución del analizador LL(1)

```
python3 ll1.py "id + id + id"
```

### Ejecución del analizador CYK

```
python3 cyk.py "id + id + id"
```

### Casos de prueba válidos

```
python3 ll1.py "id + id + id"
python3 cyk.py "id + id + id"
```

### Casos inválidos

```
python3 ll1.py "id +"
python3 cyk.py "id + + id"
```


## Benchmark

Para ejecutar la comparación de rendimiento entre ambos algoritmos:

```
python3 bench.py | tee resultados.csv
```

Este comando:
- Ejecuta múltiples pruebas con diferentes tamaños de entrada
- Mide los tiempos de ejecución de ambos algoritmos
- Guarda los resultados en `resultados.csv`


## Complejidad esperada

| Algoritmo | Complejidad temporal |
|-----------|---------------------|
| **LL(1)** | O(n)               |
| **CYK**   | O(n³)              |

### Salida esperada del benchmark

```
n_ids;cases;cyk_min;cyk_med;ll1_min;ll1_med
5;40;0.002255;0.002386;0.000079;0.000080
10;40;0.011179;0.011236;0.000152;0.000159
20;40;0.069512;0.070870;0.000288;0.000296
40;40;0.479992;0.484146;0.000513;0.000514
80;40;4.189541;4.273013;0.001182;0.001198
```

**Interpretación de las columnas:**
- `n_ids`: Número de identificadores en la cadena de prueba
- `cases`: Cantidad de casos ejecutados
- `cyk_min`: Tiempo mínimo de ejecución de CYK (segundos)
- `cyk_med`: Tiempo promedio de ejecución de CYK (segundos)
- `ll1_min`: Tiempo mínimo de ejecución de LL(1) (segundos)
- `ll1_med`: Tiempo promedio de ejecución de LL(1) (segundos)


## Observaciones

Como se puede ver en los resultados, el algoritmo **LL(1)** es significativamente más rápido que **CYK**, especialmente a medida que aumenta el tamaño de la entrada. Esto confirma las complejidades teóricas:

- LL(1) escala linealmente con el tamaño de entrada
- CYK muestra crecimiento cúbico, haciendo que el tiempo de procesamiento se dispare con entradas más grandes

## Evidencias

<img width="542" height="830" alt="imagen" src="https://github.com/user-attachments/assets/6b524e48-7f7c-4ee1-b6f4-01b6add5b711" />



















## Punto 5

# Proyecto – Analizador léxico y sintáctico de expresiones aritméticas

Este proyecto implementa un analizador **léxico** y **sintáctico** simple en Python capaz de interpretar expresiones aritméticas con suma, resta, multiplicación, división y paréntesis.


## Instalación

### 1. Crear la carpeta del proyecto

```
mkdir punto5
cd punto5
```

### 2. Crear los archivos necesarios

#### 2.1 Archivo `lexer.py`

```
nano lexer.py
```

Implementar el analizador léxico con las expresiones regulares para reconocer tokens.

#### 2.2 Archivo `parser.py`

```
nano parser.py
```

Implementar el analizador sintáctico con la gramática definida.

#### 2.3 Archivo `main.py`

```
nano main.py
```

Crear el punto de entrada que integra lexer y parser.


## Cómo ejecutar el proyecto


### 1. Entrar a la carpeta del proyecto

```
cd punto5
```

### 2. Ejecutar el programa principal

```
python3 -m punto5.main

```

El programa abre un modo interactivo tipo consola donde puedes ingresar expresiones aritméticas.


### Ejemplos de entrada válida

```
> 3 + 5
OK = 8.0

> 10 - 2 * 3
OK = 4.0

> (2 + 3) * 4
OK = 20.0

> 100 / (5 + 5)
OK = 10.0
```

### Manejo de errores

```
> (3 + )
Error: Expresión inválida en pos 4

> 5 * * 2
Error: Expresión inválida en pos 4
```

### Salir del programa

Para salir del programa, presiona **Ctrl + D**


## Explicación del funcionamiento

### `lexer.py` - Analizador Léxico

- Define expresiones regulares para reconocer tokens:
  - `NUM`: Números enteros y decimales
  - `PLUS`: Operador suma (+)
  - `MINUS`: Operador resta (-)
  - `MUL`: Operador multiplicación (*)
  - `DIV`: Operador división (/)
  - `LP`: Paréntesis izquierdo (()
  - `RP`: Paréntesis derecho ())
- Ignora espacios y saltos de línea
- Devuelve una secuencia de objetos `Token` con tipo, lexema y posición

### `parser.py` - Analizador Sintáctico

Implementa un **parser descendente recursivo** con la siguiente gramática:

```
E -> T ((PLUS|MINUS) T)*
T -> F ((MUL|DIV) F)*
F -> NUM | LP E RP
```

**Características:**
- Usa funciones `E()`, `T()`, `F()` para manejar precedencia de operadores
- Construye nodos (`Num`, `Bin`) para formar un árbol de sintaxis abstracta (AST)
- Incluye `eval_ast()` para evaluar el AST y obtener el resultado numérico
- Respeta el orden de operaciones: paréntesis > multiplicación/división > suma/resta


## Características del analizador

Soporta operaciones básicas: `+`, `-`, `*`, `/`  
Maneja paréntesis para control de precedencia  
Reconoce números enteros y decimales  
Reporta errores con posición aproximada  
Respeta el orden de operaciones matemáticas  
Interfaz interactiva tipo REPL (Read-Eval-Print-Loop)





<img width="507" height="632" alt="imagen" src="https://github.com/user-attachments/assets/8ea4eed6-28e8-47f5-bfcd-c3d71e392d79" />


