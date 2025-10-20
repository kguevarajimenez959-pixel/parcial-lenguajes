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


