#ifndef __PARSER_H
#define __PARSER_H

#include "str.h"
#include "symlist.h"
#include "arena.h"
#include "types.h"

typedef enum ParsingError : char {

    // An unknown error has occurred while parsing.
    PE_UNKNOWN = -1,

    // No error has occurred while parsing.
    PE_OK = 0,

} ParsingError;

typedef enum ExpressionType : char {
    EXPRESSION_T_UNKNOWN = 0,
    EXPRESSION_T_LIT_U8,
    EXPRESSION_T_LIT_U16,
    EXPRESSION_T_LIT_U32,
    EXPRESSION_T_LIT_U64,
} ExpressionType;

static const char* const EXPRESSION_T_NAMES[] = {
    [EXPRESSION_T_UNKNOWN] = "EXPRESSION_T_UNKNOWN",
    [EXPRESSION_T_LIT_U8] = "EXPRESSION_T_LIT_U8",
};

typedef struct Expression {
    ExpressionType type;
    struct Expression* left;
    struct Expression* right;
    bool negative;
    uint64_t int_value;
    const char* str_value;
} Expression;

typedef enum DeclarationType : char {
    DECLARATION_T_UNKNOWN = 0,
    DECLARATION_T_VARIABLE,
    DECLARATION_T_FUNCTION
} DeclarationType;

static const char* const DECLARATION_T_NAMES[] = {
    [DECLARATION_T_UNKNOWN] = "DECLARATION_T_UNKNOWN",
    [DECLARATION_T_VARIABLE] = "DECLARATION_T_VARIABLE",
    [DECLARATION_T_FUNCTION] = "DECLARATION_T_FUNCTION",
};

typedef struct Declaration {
    DeclarationType type;
    str* name;
    struct Expression* value;
    struct Statement* code;
    struct Declaration* next; // TODO: Do we want linked lists?
} Declaration;

typedef enum StatementType : char {
    STATEMENT_T_UNKNOWN
} StatementType;

static const char* const STATEMENT_T_NAMES[] = {
    [STATEMENT_T_UNKNOWN] = "STATEMENT_T_UNKNOWN",
};

typedef struct Statement {
    StatementType type;
    struct Declaration* declaration;
    struct Expression* init_expression;
    struct Expression* expression;
    struct Expression* next_expression;
    struct Statement* body;
    struct Statement* else_body;
    struct Statement* next; // TODO: Do we want linked lists?
} Statement;

/// @brief Parses the given symbol list.
/// @param arena The arena in which parsing allocation should be placed.
/// @param symlist The symbol list to be parsed.
/// @return A list of declarations.
Declaration* parse(arena* arena, SymbolList* const symlist);

Declaration* declaration_parse(arena*, SymbolList* const);
void declaration_print(const Declaration);
void declaration_type_print(const DeclarationType);
DeclarationType token_to_declaration_type(Token);

Expression* expression_parse(arena*, SymbolList* const);
void expression_print(const Expression);
void expression_type_print(const ExpressionType);

Statement* statement_parse(arena*, SymbolList* const);
void statement_print(const Statement);
void statement_type_print(const StatementType);

#endif