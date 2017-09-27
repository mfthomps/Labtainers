/* A Bison parser, made by GNU Bison 3.0.2.  */

/* Bison interface for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2013 Free Software Foundation, Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

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

#ifndef YY_YY_IEC_BISON_HH_INCLUDED
# define YY_YY_IEC_BISON_HH_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif
#if YYDEBUG
extern int yydebug;
#endif
/* "%code requires" blocks.  */
#line 255 "iec_bison.yy" /* yacc.c:1909  */

/* define a new data type to store the locations, so we can also store
 * the filename in which the token is expressed.
 */
/* NOTE: since this code will be placed in the iec_bison.hh header file,
 * as well as the iec.cc file that also includes the iec_bison.hh header file,
 * declaring the typedef struct yyltype__local here would result in a 
 * compilation error when compiling iec.cc, as this struct would be
 * declared twice.
 * We therefore use the #if !defined YYLTYPE ...
 * to make sure only the first declaration is parsed by the C++ compiler.
 */
#if ! defined YYLTYPE && ! defined YYLTYPE_IS_DECLARED
typedef struct YYLTYPE {
    int         first_line;
    int         first_column;
    const char *first_file;
    long int    first_order;
    int         last_line;
    int         last_column;
    const char *last_file;
    long int    last_order;
} YYLTYPE;
#define YYLTYPE_IS_DECLARED 1
#define YYLTYPE_IS_TRIVIAL 0
#endif


#line 73 "iec_bison.hh" /* yacc.c:1909  */

/* Token type.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    END_OF_INPUT = 0,
    BOGUS_TOKEN_ID = 258,
    prev_declared_variable_name_token = 259,
    prev_declared_direct_variable_token = 260,
    prev_declared_fb_name_token = 261,
    prev_declared_simple_type_name_token = 262,
    prev_declared_subrange_type_name_token = 263,
    prev_declared_enumerated_type_name_token = 264,
    prev_declared_array_type_name_token = 265,
    prev_declared_structure_type_name_token = 266,
    prev_declared_string_type_name_token = 267,
    prev_declared_ref_type_name_token = 268,
    prev_declared_derived_function_name_token = 269,
    prev_declared_derived_function_block_name_token = 270,
    prev_declared_program_type_name_token = 271,
    disable_code_generation_pragma_token = 272,
    enable_code_generation_pragma_token = 273,
    pragma_token = 274,
    EN = 275,
    ENO = 276,
    REF = 277,
    DREF = 278,
    REF_TO = 279,
    NULL_token = 280,
    identifier_token = 281,
    integer_token = 282,
    binary_integer_token = 283,
    octal_integer_token = 284,
    hex_integer_token = 285,
    real_token = 286,
    safeboolean_true_literal_token = 287,
    safeboolean_false_literal_token = 288,
    boolean_true_literal_token = 289,
    boolean_false_literal_token = 290,
    FALSE = 291,
    TRUE = 292,
    single_byte_character_string_token = 293,
    double_byte_character_string_token = 294,
    fixed_point_token = 295,
    fixed_point_d_token = 296,
    integer_d_token = 297,
    fixed_point_h_token = 298,
    integer_h_token = 299,
    fixed_point_m_token = 300,
    integer_m_token = 301,
    fixed_point_s_token = 302,
    integer_s_token = 303,
    fixed_point_ms_token = 304,
    integer_ms_token = 305,
    end_interval_token = 306,
    erroneous_interval_token = 307,
    T_SHARP = 308,
    D_SHARP = 309,
    BYTE = 310,
    WORD = 311,
    DWORD = 312,
    LWORD = 313,
    LREAL = 314,
    REAL = 315,
    SINT = 316,
    INT = 317,
    DINT = 318,
    LINT = 319,
    USINT = 320,
    UINT = 321,
    UDINT = 322,
    ULINT = 323,
    WSTRING = 324,
    STRING = 325,
    BOOL = 326,
    TIME = 327,
    DATE = 328,
    DATE_AND_TIME = 329,
    DT = 330,
    TIME_OF_DAY = 331,
    TOD = 332,
    SAFEBYTE = 333,
    SAFEWORD = 334,
    SAFEDWORD = 335,
    SAFELWORD = 336,
    SAFELREAL = 337,
    SAFEREAL = 338,
    SAFESINT = 339,
    SAFEINT = 340,
    SAFEDINT = 341,
    SAFELINT = 342,
    SAFEUSINT = 343,
    SAFEUINT = 344,
    SAFEUDINT = 345,
    SAFEULINT = 346,
    SAFEWSTRING = 347,
    SAFESTRING = 348,
    SAFEBOOL = 349,
    SAFETIME = 350,
    SAFEDATE = 351,
    SAFEDATE_AND_TIME = 352,
    SAFEDT = 353,
    SAFETIME_OF_DAY = 354,
    SAFETOD = 355,
    ANY = 356,
    ANY_DERIVED = 357,
    ANY_ELEMENTARY = 358,
    ANY_MAGNITUDE = 359,
    ANY_NUM = 360,
    ANY_REAL = 361,
    ANY_INT = 362,
    ANY_BIT = 363,
    ANY_STRING = 364,
    ANY_DATE = 365,
    ASSIGN = 366,
    DOTDOT = 367,
    TYPE = 368,
    END_TYPE = 369,
    ARRAY = 370,
    OF = 371,
    STRUCT = 372,
    END_STRUCT = 373,
    direct_variable_token = 374,
    incompl_location_token = 375,
    VAR_INPUT = 376,
    VAR_OUTPUT = 377,
    VAR_IN_OUT = 378,
    VAR_EXTERNAL = 379,
    VAR_GLOBAL = 380,
    END_VAR = 381,
    RETAIN = 382,
    NON_RETAIN = 383,
    R_EDGE = 384,
    F_EDGE = 385,
    AT = 386,
    standard_function_name_token = 387,
    FUNCTION = 388,
    END_FUNCTION = 389,
    CONSTANT = 390,
    standard_function_block_name_token = 391,
    FUNCTION_BLOCK = 392,
    END_FUNCTION_BLOCK = 393,
    VAR_TEMP = 394,
    VAR = 395,
    PROGRAM = 396,
    END_PROGRAM = 397,
    ACTION = 398,
    END_ACTION = 399,
    TRANSITION = 400,
    END_TRANSITION = 401,
    FROM = 402,
    TO = 403,
    PRIORITY = 404,
    INITIAL_STEP = 405,
    STEP = 406,
    END_STEP = 407,
    L = 408,
    D = 409,
    SD = 410,
    DS = 411,
    SL = 412,
    N = 413,
    P = 414,
    P0 = 415,
    P1 = 416,
    prev_declared_global_var_name_token = 417,
    prev_declared_program_name_token = 418,
    prev_declared_resource_name_token = 419,
    prev_declared_configuration_name_token = 420,
    CONFIGURATION = 421,
    END_CONFIGURATION = 422,
    TASK = 423,
    RESOURCE = 424,
    ON = 425,
    END_RESOURCE = 426,
    VAR_CONFIG = 427,
    VAR_ACCESS = 428,
    WITH = 429,
    SINGLE = 430,
    INTERVAL = 431,
    READ_WRITE = 432,
    READ_ONLY = 433,
    EOL = 434,
    sendto_identifier_token = 435,
    LD = 436,
    LDN = 437,
    ST = 438,
    STN = 439,
    NOT = 440,
    S = 441,
    R = 442,
    S1 = 443,
    R1 = 444,
    CLK = 445,
    CU = 446,
    CD = 447,
    PV = 448,
    IN = 449,
    PT = 450,
    AND = 451,
    AND2 = 452,
    OR = 453,
    XOR = 454,
    ANDN = 455,
    ANDN2 = 456,
    ORN = 457,
    XORN = 458,
    ADD = 459,
    SUB = 460,
    MUL = 461,
    DIV = 462,
    MOD = 463,
    GT = 464,
    GE = 465,
    EQ = 466,
    LT = 467,
    LE = 468,
    NE = 469,
    CAL = 470,
    CALC = 471,
    CALCN = 472,
    RET = 473,
    RETC = 474,
    RETCN = 475,
    JMP = 476,
    JMPC = 477,
    JMPCN = 478,
    SENDTO = 479,
    OPER_NE = 480,
    OPER_GE = 481,
    OPER_LE = 482,
    OPER_EXP = 483,
    RETURN = 484,
    IF = 485,
    THEN = 486,
    ELSIF = 487,
    ELSE = 488,
    END_IF = 489,
    CASE = 490,
    END_CASE = 491,
    FOR = 492,
    BY = 493,
    DO = 494,
    END_FOR = 495,
    WHILE = 496,
    END_WHILE = 497,
    REPEAT = 498,
    UNTIL = 499,
    END_REPEAT = 500,
    EXIT = 501
  };
#endif
/* Tokens.  */
#define END_OF_INPUT 0
#define BOGUS_TOKEN_ID 258
#define prev_declared_variable_name_token 259
#define prev_declared_direct_variable_token 260
#define prev_declared_fb_name_token 261
#define prev_declared_simple_type_name_token 262
#define prev_declared_subrange_type_name_token 263
#define prev_declared_enumerated_type_name_token 264
#define prev_declared_array_type_name_token 265
#define prev_declared_structure_type_name_token 266
#define prev_declared_string_type_name_token 267
#define prev_declared_ref_type_name_token 268
#define prev_declared_derived_function_name_token 269
#define prev_declared_derived_function_block_name_token 270
#define prev_declared_program_type_name_token 271
#define disable_code_generation_pragma_token 272
#define enable_code_generation_pragma_token 273
#define pragma_token 274
#define EN 275
#define ENO 276
#define REF 277
#define DREF 278
#define REF_TO 279
#define NULL_token 280
#define identifier_token 281
#define integer_token 282
#define binary_integer_token 283
#define octal_integer_token 284
#define hex_integer_token 285
#define real_token 286
#define safeboolean_true_literal_token 287
#define safeboolean_false_literal_token 288
#define boolean_true_literal_token 289
#define boolean_false_literal_token 290
#define FALSE 291
#define TRUE 292
#define single_byte_character_string_token 293
#define double_byte_character_string_token 294
#define fixed_point_token 295
#define fixed_point_d_token 296
#define integer_d_token 297
#define fixed_point_h_token 298
#define integer_h_token 299
#define fixed_point_m_token 300
#define integer_m_token 301
#define fixed_point_s_token 302
#define integer_s_token 303
#define fixed_point_ms_token 304
#define integer_ms_token 305
#define end_interval_token 306
#define erroneous_interval_token 307
#define T_SHARP 308
#define D_SHARP 309
#define BYTE 310
#define WORD 311
#define DWORD 312
#define LWORD 313
#define LREAL 314
#define REAL 315
#define SINT 316
#define INT 317
#define DINT 318
#define LINT 319
#define USINT 320
#define UINT 321
#define UDINT 322
#define ULINT 323
#define WSTRING 324
#define STRING 325
#define BOOL 326
#define TIME 327
#define DATE 328
#define DATE_AND_TIME 329
#define DT 330
#define TIME_OF_DAY 331
#define TOD 332
#define SAFEBYTE 333
#define SAFEWORD 334
#define SAFEDWORD 335
#define SAFELWORD 336
#define SAFELREAL 337
#define SAFEREAL 338
#define SAFESINT 339
#define SAFEINT 340
#define SAFEDINT 341
#define SAFELINT 342
#define SAFEUSINT 343
#define SAFEUINT 344
#define SAFEUDINT 345
#define SAFEULINT 346
#define SAFEWSTRING 347
#define SAFESTRING 348
#define SAFEBOOL 349
#define SAFETIME 350
#define SAFEDATE 351
#define SAFEDATE_AND_TIME 352
#define SAFEDT 353
#define SAFETIME_OF_DAY 354
#define SAFETOD 355
#define ANY 356
#define ANY_DERIVED 357
#define ANY_ELEMENTARY 358
#define ANY_MAGNITUDE 359
#define ANY_NUM 360
#define ANY_REAL 361
#define ANY_INT 362
#define ANY_BIT 363
#define ANY_STRING 364
#define ANY_DATE 365
#define ASSIGN 366
#define DOTDOT 367
#define TYPE 368
#define END_TYPE 369
#define ARRAY 370
#define OF 371
#define STRUCT 372
#define END_STRUCT 373
#define direct_variable_token 374
#define incompl_location_token 375
#define VAR_INPUT 376
#define VAR_OUTPUT 377
#define VAR_IN_OUT 378
#define VAR_EXTERNAL 379
#define VAR_GLOBAL 380
#define END_VAR 381
#define RETAIN 382
#define NON_RETAIN 383
#define R_EDGE 384
#define F_EDGE 385
#define AT 386
#define standard_function_name_token 387
#define FUNCTION 388
#define END_FUNCTION 389
#define CONSTANT 390
#define standard_function_block_name_token 391
#define FUNCTION_BLOCK 392
#define END_FUNCTION_BLOCK 393
#define VAR_TEMP 394
#define VAR 395
#define PROGRAM 396
#define END_PROGRAM 397
#define ACTION 398
#define END_ACTION 399
#define TRANSITION 400
#define END_TRANSITION 401
#define FROM 402
#define TO 403
#define PRIORITY 404
#define INITIAL_STEP 405
#define STEP 406
#define END_STEP 407
#define L 408
#define D 409
#define SD 410
#define DS 411
#define SL 412
#define N 413
#define P 414
#define P0 415
#define P1 416
#define prev_declared_global_var_name_token 417
#define prev_declared_program_name_token 418
#define prev_declared_resource_name_token 419
#define prev_declared_configuration_name_token 420
#define CONFIGURATION 421
#define END_CONFIGURATION 422
#define TASK 423
#define RESOURCE 424
#define ON 425
#define END_RESOURCE 426
#define VAR_CONFIG 427
#define VAR_ACCESS 428
#define WITH 429
#define SINGLE 430
#define INTERVAL 431
#define READ_WRITE 432
#define READ_ONLY 433
#define EOL 434
#define sendto_identifier_token 435
#define LD 436
#define LDN 437
#define ST 438
#define STN 439
#define NOT 440
#define S 441
#define R 442
#define S1 443
#define R1 444
#define CLK 445
#define CU 446
#define CD 447
#define PV 448
#define IN 449
#define PT 450
#define AND 451
#define AND2 452
#define OR 453
#define XOR 454
#define ANDN 455
#define ANDN2 456
#define ORN 457
#define XORN 458
#define ADD 459
#define SUB 460
#define MUL 461
#define DIV 462
#define MOD 463
#define GT 464
#define GE 465
#define EQ 466
#define LT 467
#define LE 468
#define NE 469
#define CAL 470
#define CALC 471
#define CALCN 472
#define RET 473
#define RETC 474
#define RETCN 475
#define JMP 476
#define JMPC 477
#define JMPCN 478
#define SENDTO 479
#define OPER_NE 480
#define OPER_GE 481
#define OPER_LE 482
#define OPER_EXP 483
#define RETURN 484
#define IF 485
#define THEN 486
#define ELSIF 487
#define ELSE 488
#define END_IF 489
#define CASE 490
#define END_CASE 491
#define FOR 492
#define BY 493
#define DO 494
#define END_FOR 495
#define WHILE 496
#define END_WHILE 497
#define REPEAT 498
#define UNTIL 499
#define END_REPEAT 500
#define EXIT 501

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
typedef union YYSTYPE YYSTYPE;
union YYSTYPE
{
#line 286 "iec_bison.yy" /* yacc.c:1909  */

    symbol_c 	*leaf;
    list_c	*list;
    char 	*ID;	/* token value */

#line 585 "iec_bison.hh" /* yacc.c:1909  */
};
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif

/* Location type.  */
#if ! defined YYLTYPE && ! defined YYLTYPE_IS_DECLARED
typedef struct YYLTYPE YYLTYPE;
struct YYLTYPE
{
  int first_line;
  int first_column;
  int last_line;
  int last_column;
};
# define YYLTYPE_IS_DECLARED 1
# define YYLTYPE_IS_TRIVIAL 1
#endif


extern YYSTYPE yylval;
extern YYLTYPE yylloc;
int yyparse (void);

#endif /* !YY_YY_IEC_BISON_HH_INCLUDED  */
