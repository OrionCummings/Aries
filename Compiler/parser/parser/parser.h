#ifndef __PARSER_H
#define __PARSER_H

#include "str.h"
#include "symlist.h"
#include "arena.h"

typedef enum parsing_error_t : char {

    // An unknown error has occurred while parsing.
    PE_UNKNOWN = -1,

    // No error has occurred while parsing.
    PE_OK = 0,

} parsing_error_t;

typedef enum BuiltinType : char {
    BITYPE_UNKNOWN,
    BITYPE_VOID,
    BITYPE_BOOL,
    BITYPE_U8,
    BITYPE_U16,
    BITYPE_U32,
    BITYPE_U64,
    BITYPE_I8,
    BITYPE_I16,
    BITYPE_I32,
    BITYPE_I64,
    BITYPE_F32,
    BITYPE_F64,
    BITYPE_OPT,
    BITYPE_RES,
    BITYPE_STR,
} BuiltinType;

typedef enum ExpressionType : char {
    EXPR_T_UNKNOWN = 0,
    EXPR_T_LIT_INT
} ExpressionType;

static const char* const EXPR_T_NAMES[] = {
    [EXPR_T_UNKNOWN] = "EXPR_T_UNKNOWN",
    [EXPR_T_LIT_INT] = "EXPR_T_LIT_INT",
};

typedef enum StatementType : char {
    STMT_T_UNKNOWN
} StatementType;

static const char* const STMT_T_NAMES[] = {
    [STMT_T_UNKNOWN] = "STMT_T_UNKNOWN",
};

typedef enum DeclarationType : char {
    DECL_T_UNKNOWN = 0,
    DECL_T_VARIABLE,
    DECL_T_FUNCTION
} DeclarationType;

static const char* const DECL_T_NAMES[] = {
    [DECL_T_UNKNOWN] = "DECL_T_UNKNOWN",
    [DECL_T_VARIABLE] = "DECL_T_VARIABLE",
    [DECL_T_FUNCTION] = "DECL_T_FUNCTION",
};

typedef struct Expression {
    ExpressionType type;
    struct Expression* left;
    struct Expression* right;
    bool negative;
    uint64_t int_value;
    const char* str_value;
} Expression;

typedef struct Statement {
    StatementType type;
    struct Declaration* decl;
    struct Expression* init_expr;
    struct Expression* expr;
    struct Expression* next_expr;
    struct Statement* body;
    struct Statement* else_body;
    struct Statement* next; // TODO: Do we want linked lists?
} Statement;

typedef struct Declaration {
    DeclarationType type;
    str* name;
    struct Expression* value;
    struct Statement* code;
    struct Declaration* next; // TODO: Do we want linked lists?
} Declaration;

// High-level functions

/// @brief Parses the given symbol list.
/// @param arena The arena in which parsing allocation should be placed.
/// @param symlist The symbol list to be parsed.
/// @return A list of declarations.
Declaration* parse(arena* arena, SymbolList* const symlist);

Declaration* decl_parse(arena* arena, SymbolList* const symlist);
Statement* stmt_parse(arena* arena, SymbolList* const symlist);
Expression* expr_parse(arena* arena, SymbolList* const symlist);

// Utility functions
void decl_print(const Declaration decl);
void decl_type_print(const DeclarationType decl_type);
void stmt_print(const Statement stmt);
void stmt_type_print(const StatementType stmt_type);
void expr_print(const Expression expr);
void expr_type_print(const ExpressionType expr_type);


DeclarationType token_to_decl_type(Token t);

#endif