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

