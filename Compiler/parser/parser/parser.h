#ifndef __PARSER_H
#define __PARSER_H

#include "arena.h"
#include "str.h"
#include "symlist.h"
#include "types.h"

// ???????????????
// typedef struct {
//     bool terminal;
//     const char* id;
//     const char* production;
//     bool (*func)(const char*);
// } Rule;

// static const Rule rules[] = {
//     (Rule){ .terminal = false, .id = "NumericExpression", .production = "Number BinaryOperation Number" },
//     (Rule){ .terminal = false, .id = "NumericExpression",                        .production = "Number" },
//     (Rule){ .terminal = false,            .id = "Number",                         .production = "Digit" },
// };

// typedef struct {

// } parsing_stack;

typedef enum ParsingError : int8_t {

    // An unknown error has occurred while parsing.
    PE_UNKNOWN = -1,

    // No error has occurred while parsing.
    PE_OK = 0,

} ParsingError;

typedef enum ExpressionType : uint8_t {
    ET_UNKNOWN = 0,
    ET_LIT_U8,
    ET_LIT_U16,
    ET_LIT_U32,
    ET_LIT_U64,
    ET_BIN_OP_ADD,
} ExpressionType;

typedef struct Expression {
    ExpressionType type;
    str* value;
    struct Expression* left;
    struct Expression* right;
} Expression;

typedef enum DeclarationType : char { DT_UNKNOWN = 0, DT_VARIABLE, DT_FUNCTION } DeclarationType;

typedef struct Declaration {
    DeclarationType type;
    str* name;
    struct Expression* value;
    struct Statement* code;
    struct Declaration* next; // TODO: Do we want linked lists?
} Declaration;

typedef enum StatementType : char { ST_UNKNOWN } StatementType;

static const char* const ET_NAMES[] = {
    [ET_UNKNOWN] = "ET_UNKNOWN",
    [ET_LIT_U8] = "ET_LIT_U8",
    [ET_BIN_OP_ADD] = "ET_BIN_OP_ADD",
};

static const char* const DT_NAMES[] = {
    [DT_UNKNOWN] = "DT_UNKNOWN",
    [DT_VARIABLE] = "DT_VARIABLE",
    [DT_FUNCTION] = "DT_FUNCTION",
};

static const char* const ST_NAMES[] = {
    [ST_UNKNOWN] = "ST_UNKNOWN",
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
Declaration* parse(arena* arena, symlist* const symlist);

Declaration* declaration_parse(arena*, symlist* const);
void declaration_print(const Declaration);
void declaration_type_print(const DeclarationType);
DeclarationType token_to_declaration_type(TokenType);

Expression* expression_parse(arena*, symlist* const, index_t);
Expression* expression_new(arena*, ExpressionType, str*);
bool expression_eq(const Expression* const e1, const Expression* const e2);
void expression_print(const Expression, size_t);
void expression_type_print(const ExpressionType);
bool valid_start_expression(TokenType);

Statement* statement_parse(arena*, symlist* const);
void statement_print(const Statement);
void statement_type_print(const StatementType);

#endif