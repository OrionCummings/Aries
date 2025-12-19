#ifndef __PARSER_H
#define __PARSER_H

#include "str.h"
#include "sym_list.h"
#include "arena.h"

typedef enum {
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

typedef enum {
    ASTV_UNKNOWN,
    ASTV_DECLARATION,
    ASTV_STATEMENT,
    ASTV_EXPRESSION,
} ASTNodeVariant;

typedef struct {
    void* test;
} Expression;

typedef enum {
    STMT_T_UNKNOWN
} StatementType;

typedef struct {
    StatementType type;

} Statement;

typedef enum {
    DT_UNKNOWN,
    DT_VARIABLE,
    DT_FUNCTION
} DeclarationType;

typedef struct {
    str* name;
    DeclarationType type;
    Expression expr;
    Statement statement;
    struct Declaration* next;
} Declaration;

typedef struct {
    ASTNodeVariant var;
    struct ASTNode* children;
} ASTNode;

// High-level functions
ASTNode* parse(const SymbolList* const symlist);

// Memory functions
Declaration* decl_anew(const arena* a, const str* name, const DeclarationType type, const Expression* expr, const Statement* stmt, const Declaration* next);
Expression* expr_anew();
Statement* stmt_anew();

// Utility functions
void astnode_print(const ASTNode* const node);



#endif