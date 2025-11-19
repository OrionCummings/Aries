#ifndef __PARSER_H
#define __PARSER_H

#include "str.h"

typedef enum {
    TYPE_UNKNOWN,
    TYPE_VOID,
    TYPE_BOOL,
    TYPE_U8,
    TYPE_U16,
    TYPE_U32,
    TYPE_U64,
    TYPE_I8,
    TYPE_I16,
    TYPE_I32,
    TYPE_I64,
    TYPE_F32,
    TYPE_F64,
    TYPE_OPT,
    TYPE_RES,
    TYPE_STR,
}BuiltinType;

typedef enum {
    UNKNOWN_AST_NODE_VARIANT,
    DECLARATION,
    STATEMENT,
    EXPRESSION,
} ASTNodeVariant;

typedef enum {
    UNKNOWN_DECLARATION_TYPE,
    VARIABLE

} DeclarationType;

typedef struct {
    str* name;
    BuiltinType type;
    struct ParameterList* next;
} ParameterList;

typedef struct {
    ASTNodeVariant var;
    struct ASTNode* children;
} ASTNode;

typedef struct {
    ASTNode ast;
    bool complete;

} Parser;

// Parser* parser_new(const SymList* const sym_list);
void _parser_free(Parser* parser);
#define parser_free(p) \
do {                   \
    _parser_free(p);   \
    p = NULL;          \
} while (0)

bool parse(Parser* parser);
void parser_print(const Parser* const parser);

#endif