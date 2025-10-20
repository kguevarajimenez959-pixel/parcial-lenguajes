# PARCIAL LENGUAJES
## Punto 1 
Diseñar una gramática de un lenguaje de Programación que permita hacer las operaciones de CRUD en una base de datos.

```txt
Programa        = { Sentencia ";" } ;

Sentencia       = Crear | Leer | Actualizar | Borrar ;

Crear           = "CREATE" "INTO" Ident "(" CamposVal ")" ;
CamposVal       = CampoVal { "," CampoVal } ;
CampoVal        = Ident ":" Exp ;

Leer            = "READ" "FROM" Ident [ Seleccion ] [ Filtro ] [ Orden ] [ Limite ] ;
Seleccion       = "SELECT" ( "*" | ListaIdent ) ;
Filtro          = "WHERE" ExprBool ;
Orden           = "ORDER" "BY" Ordenes ;
Ordenes         = OrdenElem { "," OrdenElem } ;
OrdenElem       = Ident [ "ASC" | "DESC" ] ;
Limite          = "LIMIT" Entero ;

Actualizar      = "UPDATE" Ident "SET" Asignaciones [ Filtro ] ;
Asignaciones    = Asign { "," Asign } ;
Asign           = Ident "=" Exp ;

Borrar          = "DELETE" "FROM" Ident [ Filtro ] ;

/* Expresiones */
Exp             = Literal
                | Ident
                | Llamado
                | "(" Exp ")"
                | Exp "+" Exp
                | Exp "-" Exp
                | Exp "*" Exp
                | Exp "/" Exp ;

ExprBool        = BoolTerm { "OR" BoolTerm } ;
BoolTerm        = BoolFact { "AND" BoolFact } ;
BoolFact        = [ "NOT" ] BoolAtom ;
BoolAtom        = "(" ExprBool ")"
                | Comparacion ;
Comparacion     = Exp OpComp Exp ;
OpComp          = "=" | "!=" | "<" | "<=" | ">" | ">=" | "LIKE" | "IN" ;

/* Listas y llamados */
ListaIdent      = Ident { "," Ident } ;
Llamado         = Ident "(" [ ListaArgs ] ")" ;
ListaArgs       = Exp { "," Exp } ;

/* Léxicos */
Ident           = Letra { Letra | Digito | "_" } ;
Entero          = Digito { Digito } ;
Real            = Entero "." Entero ;
Cadena          = "\"" { Caracter } "\"" ;
Booleano        = "TRUE" | "FALSE" ;
Nulo            = "NULL" ;

Literal         = Cadena | Real | Entero | Booleano | Nulo ;

Letra           = "A"…"Z" | "a"…"z" ;
Digito          = "0"…"9" ;
Caracter        = cualquier carácter excepto comillas dobles o salto de línea ;
```
## Punto 2
Implemente la gramatica del punto 1 en Bison o ANTLR y realice pruebas sobre el lenguaje

## Archivo Bison
```bison
/* crud.y */
%{
  #include <stdio.h>
  #include <stdlib.h>

  void yyerror(const char *s);
  int yylex(void);
  extern int yylineno;  /* usar la variable del lexer, no redefinirla */
%}

/* ====== Precedencias y asociatividades ====== */
%left OR
%left AND
%right NOT
%left LIKE IN
%left EQ NEQ LT LE GT GE
%left '+' '-'
%left '*' '/'
%right UMINUS

/* ====== Tokens ====== */
%token CREATE INTO READ FROM SELECT WHERE ORDER BYTK LIMIT
%token UPDATE SET DELETE
%token ASC DESC TRUE_T FALSE_T NULL_T
%token IDENT STRING
%token INT REAL
%token LIKE IN
%token EQ NEQ LT LE GT GE
%token AND OR NOT
%token '(' ')' ',' ';' ':' '+' '-' '*' '/'

%%

/* ====== Reglas de la gramática ====== */

programa
  : /* vacío */
  | programa sentencia ';'
  ;

sentencia
  : crear
  | leer
  | actualizar
  | borrar
  ;

/* CREATE INTO tabla (campo: valor, ...) */
crear
  : CREATE INTO IDENT '(' campos_val ')'
  ;

campos_val
  : campo_val
  | campos_val ',' campo_val
  ;

campo_val
  : IDENT ':' expr
  ;

/* READ FROM tabla [SELECT ...] [WHERE ...] [ORDER BY ...] [LIMIT ...] */
leer
  : READ FROM IDENT opt_seleccion opt_filtro opt_orden opt_limite
  ;

opt_seleccion
  : /* vacío */
  | SELECT '*'
  | SELECT lista_ident
  ;

opt_filtro
  : /* vacío */
  | WHERE expr_bool
  ;

opt_orden
  : /* vacío */
  | ORDER BYTK ordenes
  ;

ordenes
  : orden_elem
  | ordenes ',' orden_elem
  ;

orden_elem
  : IDENT
  | IDENT ASC
  | IDENT DESC
  ;

opt_limite
  : /* vacío */
  | LIMIT INT
  ;

/* UPDATE tabla SET campo=expr, ... [WHERE ...] */
actualizar
  : UPDATE IDENT SET asignaciones opt_filtro
  ;

asignaciones
  : asign
  | asignaciones ',' asign
  ;

asign
  : IDENT '=' expr
  ;

/* DELETE FROM tabla [WHERE ...] */
borrar
  : DELETE FROM IDENT opt_filtro
  ;

/* ====== Expresiones ====== */

expr
  : literal
  | IDENT
  | llamado
  | '(' expr ')'
  | expr '+' expr
  | expr '-' expr
  | expr '*' expr
  | expr '/' expr
  | '-' expr %prec UMINUS
  ;

llamado
  : IDENT '(' ')'
  | IDENT '(' lista_args ')'
  ;

lista_args
  : expr
  | lista_args ',' expr
  ;

/* ====== Expresiones booleanas ====== */

expr_bool
  : bool_term
  | expr_bool OR bool_term
  ;

bool_term
  : bool_fact
  | bool_term AND bool_fact
  ;

bool_fact
  : bool_atom
  | NOT bool_atom
  ;

bool_atom
  : '(' expr_bool ')'
  | comparacion
  ;

comparacion
  : expr opcomp expr
  | expr LIKE expr
  | expr IN '(' lista_args ')'
  ;

opcomp
  : EQ | NEQ | LT | LE | GT | GE
  ;

/* ====== Listas e identificadores ====== */

lista_ident
  : IDENT
  | lista_ident ',' IDENT
  ;

/* ====== Literales ====== */

literal
  : STRING
  | REAL
  | INT
  | TRUE_T
  | FALSE_T
  | NULL_T
  ;

%%

/* ====== Código C adicional ====== */

void yyerror(const char *s) {
  fprintf(stderr, "Error de sintaxis en línea %d: %s\n", yylineno, s);
}

int main(void) {
  if (yyparse() == 0)
    printf("OK: programa válido\n");
  return 0;
}
```
## Archivo Flex
```txt
%option noyywrap
%option caseless
%{
  #include "crud.tab.h"
  #include <string.h>
  extern int yylineno;   /* se usa, no se redefine */
%}

/* ====== Expresiones regulares ====== */
WS        [ \t\r]+
ID        [A-Za-z_][A-Za-z0-9_]*
INTLIT    [0-9]+
REALLIT   [0-9]+\.[0-9]+
STRLIT    \"([^\"\n]|\\.)*\"

%%
\n                  { yylineno++; }
{WS}                { /* ignora espacios */ }


CREATE              { return CREATE; }
INTO                { return INTO; }
READ                { return READ; }
FROM                { return FROM; }
SELECT              { return SELECT; }
WHERE               { return WHERE; }
ORDER               { return ORDER; }
BY                  { return BYTK; }
LIMIT               { return LIMIT; }
UPDATE              { return UPDATE; }
SET                 { return SET; }
DELETE              { return DELETE; }
ASC                 { return ASC; }
DESC                { return DESC; }
TRUE                { return TRUE_T; }
FALSE               { return FALSE_T; }
NULL                { return NULL_T; }
LIKE                { return LIKE; }
IN                  { return IN; }
AND                 { return AND; }
OR                  { return OR; }
NOT                 { return NOT; }


"="                 { return EQ; }
"!="                { return NEQ; }
"<="                { return LE; }
">="                { return GE; }
"<"                 { return LT; }
">"                 { return GT; }
","                 { return ','; }
";"                 { return ';'; }
"("                 { return '('; }
")"                 { return ')'; }
":"                 { return ':'; }
"+"                 { return '+'; }
"-"                 { return '-'; }
"*"                 { return '*'; }
"/"                 { return '/'; }


{REALLIT}           { return REAL; }
{INTLIT}            { return INT; }
{STRLIT}            { return STRING; }
{ID}                { return IDENT; }


.                   { return yytext[0]; }
%%
```

## Txt de Prueba

## Punto 3

## Objetivo

Implementar un analizador sintáctico **ascendente** para la gramática de expresiones:

```
E → E + T | T
T → T * F | F
F → ( E ) | id
```

y documentar: transformación a **LL(1)**, **FIRST**, **FOLLOW**, **PREDICT**, algoritmo con **pila**, y pruebas. 


## 1) Gramática de partida y transformación a LL(1)

### 1.1 Gramática original

```
E → E + T | T
T → T * F | F
F → ( E ) | id
```

Contiene recursión izquierda inmediata en `E` y `T`. 

### 1.2 Gramática LL(1) resultante

Eliminando recursión izquierda y usando no terminales auxiliares:

```
E  → T E'
E' → + T E' | ε
T  → F T'
T' → * F T' | ε
F  → ( E ) | id
```


## 2) Conjuntos FIRST, FOLLOW y PREDICT

El proyecto calcula los conjuntos de forma genérica:

* **FIRST** para símbolos y secuencias.
* **FOLLOW** para no terminales con `EOF = $`.
* **PREDICT** para cada producción, combinando FIRST(α) y FOLLOW(A) cuando procede `ε`.

Implementación en `first_follow_predict.py`. Constantes en `constantes.py`.  


## 3) Analizador **ascendente** basado en pila

Se usa un **parser SLR(1)**:

1. Construcción de colección canónica de **items LR(0)**: `cierre` y `ir_a`.
2. Construcción de **tablas ACTION/GOTO** con **FOLLOW** para reducciones.
3. Bucle de análisis con **pila de estados**, acción **shift/reduce/accept**.

Construcción de tablas: `construccion_slr.py`. Ejecución del parser: `parse_slr` en `scanner_parser.py`.  

Tokenización mínima: `id`, `+`, `*`, `(`, `)`, y fin `$`. 

---

## 4) Estructura del proyecto

* `gramatica.txt`: gramática original en formato texto. 
* `constantes.py`: `EPS = "ε"`, `EOF = "$"`. 
* `utilidades_gramatica.py`: parser de gramáticas y **LL(1) estándar**. 
* `first_follow_predict.py`: FIRST, FOLLOW, PREDICT. 
* `construccion_slr.py`: colección canónica y tablas SLR(1). 
* `scanner_parser.py`: escáner, `parse_slr`, trazas LL(1). 
* `funciones.py`: reexporta utilidades para `main.py`. 
* `main.py`: interfaz CLI. 

---

## 5) Uso rápido

### 5.1 Mostrar gramáticas (original y LL(1))

```bash
python main.py --info
```
### 5.2 Mostrar Frist, Follow, predict, etc

```bash
python main.py 
```
(Despues de ejecutar poner que analizar, ej: id + id + id)

Imprime la gramática de `gramatica.txt` y la LL(1) fija. 


## 6) Pruebas sugeridas

Aceptadas:

```
id
(id)
id + id
id * id
id + id * id
(id + id) * id
```

Rechazadas:

```
+
id +
* id
(id
id * * id
```


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


## Evidencias


<img width="507" height="632" alt="imagen" src="https://github.com/user-attachments/assets/8ea4eed6-28e8-47f5-bfcd-c3d71e392d79" />


