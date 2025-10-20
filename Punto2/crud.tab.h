/* A Bison parser, made by GNU Bison 3.8.2.  */

/* Bison interface for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2015, 2018-2021 Free Software Foundation,
   Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <https://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* DO NOT RELY ON FEATURES THAT ARE NOT DOCUMENTED in the manual,
   especially those whose name start with YY_ or yy_.  They are
   private implementation details that can be changed or removed.  */

#ifndef YY_YY_CRUD_TAB_H_INCLUDED
# define YY_YY_CRUD_TAB_H_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif
#if YYDEBUG
extern int yydebug;
#endif

/* Token kinds.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    YYEMPTY = -2,
    YYEOF = 0,                     /* "end of file"  */
    YYerror = 256,                 /* error  */
    YYUNDEF = 257,                 /* "invalid token"  */
    UMINUS = 258,                  /* UMINUS  */
    CREATE = 259,                  /* CREATE  */
    INTO = 260,                    /* INTO  */
    READ = 261,                    /* READ  */
    FROM = 262,                    /* FROM  */
    SELECT = 263,                  /* SELECT  */
    WHERE = 264,                   /* WHERE  */
    ORDER = 265,                   /* ORDER  */
    BYTK = 266,                    /* BYTK  */
    LIMIT = 267,                   /* LIMIT  */
    UPDATE = 268,                  /* UPDATE  */
    SET = 269,                     /* SET  */
    DELETE = 270,                  /* DELETE  */
    ASC = 271,                     /* ASC  */
    DESC = 272,                    /* DESC  */
    TRUE_T = 273,                  /* TRUE_T  */
    FALSE_T = 274,                 /* FALSE_T  */
    NULL_T = 275,                  /* NULL_T  */
    IDENT = 276,                   /* IDENT  */
    STRING = 277,                  /* STRING  */
    INT = 278,                     /* INT  */
    REAL = 279,                    /* REAL  */
    LIKE = 280,                    /* LIKE  */
    IN = 281,                      /* IN  */
    EQ = 282,                      /* EQ  */
    NEQ = 283,                     /* NEQ  */
    LT = 284,                      /* LT  */
    LE = 285,                      /* LE  */
    GT = 286,                      /* GT  */
    GE = 287,                      /* GE  */
    AND = 288,                     /* AND  */
    OR = 289,                      /* OR  */
    NOT = 290                      /* NOT  */
  };
  typedef enum yytokentype yytoken_kind_t;
#endif

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
typedef int YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif


extern YYSTYPE yylval;


int yyparse (void);


#endif /* !YY_YY_CRUD_TAB_H_INCLUDED  */
