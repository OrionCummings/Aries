#include "parser.h"

Declaration* parse(arena* arena, SymbolList* const symlist) {

    // TODO: This is a rather inefficient check but I think it's safe for now. Reevaluate later!
    if (!symlist_valid(symlist)) {
        A_ERROR("cannot parse an invalid symlist");
        return NULL;
    }

    return declaration_parse(arena, symlist); // NOTE: This is correct, but not for current testing!
}

Declaration* declaration_parse(arena* arena, SymbolList* const symlist) {

    // TODO: Add some bounds checking to the symlist base and look-ahead indices.

    // while (symlist->length < symlist->capacity) { // TODO: This seems flawed!

    Declaration* declaration = arena_alloc(arena, sizeof(*declaration));

    if (!declaration) {
        A_WARNING("failed to allocate from arena");
        return NULL;
    }

    // Get the base symbol and the look-ahead symbol.
    Symbol base_sym = symlist->symbols[symlist->base_index];

    if (sym_is_built_in_type(base_sym)) {

        // TODO: Add bounds checking!
        // TODO: Add identifier validation!
        // TODO: Determine if this is memory-safe (probably not!)
        str* varname = symlist->symbols[symlist->base_index + 1].s;
        if (!varname) {
            A_WARNING("failed to get declaration name");
            return NULL;
        }
        declaration->name = varname;

        DeclarationType type = token_to_declaration_type(base_sym.t);
        if (type == DECLARATION_T_UNKNOWN) {
            A_WARNING("failed to convert token to declaration type");
            return NULL;
        }
        declaration->type = type;

        // TODO: Should we accept non-initialized variables?
        // Example: "u32 x;" <-- should this be acceptable? Methinks not.

        symlist->base_index += 3; // Skip ahead 3 symbols (<type> <name> <symbol> <expression>)
        Expression* value = expression_parse(arena, symlist);
        if (!value) {
            A_WARNING("failed to parse expressionession");
            return NULL;
        }
        declaration->value = value;

        return declaration;
    }

    return NULL;
}

Expression* expression_parse(arena* arena, SymbolList* const symlist) {

    // TODO: Add some bounds checking to the symlist base and look-ahead indices.
    if (arena == NULL) { A_WARNING("invalid arena"); return NULL; }
    if (symlist == NULL) { A_WARNING("invalid symlist"); return NULL; }
    if (symlist->symbols == NULL) { A_WARNING("invalid symlist->symbols"); return NULL; }
    if (symlist->la_index > symlist->length) { A_WARNING("invalid symlist la index"); return NULL; }

    Expression* expression = arena_alloc(arena, sizeof(*expression));
    if (!expression) { A_WARNING("failed to allocate memory for an expression"); return NULL; }

    Symbol sym = symlist->symbols[symlist->base_index];
    if (!sym_valid(sym)) { A_WARNING("failed to get valid symbol"); return NULL; }

    sym_print(sym);

    // TODO: Assess if this ownership transfer is a good idea.
    expression->value = sym.s;

    switch (sym.t) {

        case(SYM_PAREN_OPEN): {

            // Increment the look ahead index!
            symlist->la_index++;
            Expression* e = expression_parse(arena, symlist);
            if (!e) {
                A_WARNING("failed to allocate memory for an expression");
                return NULL;
            }
        }

        case(LIT_U8):
            expression->type = EXPRESSION_T_LIT_U8;
        case(LIT_U16):
            expression->type = EXPRESSION_T_LIT_U16;
        case(LIT_U32):
            expression->type = EXPRESSION_T_LIT_U32;
        case(LIT_U64): {
            expression->type = EXPRESSION_T_LIT_U64;
        }
    }

    return expression;
}

void declaration_print(const Declaration declaration) {
    printf("[D]: ");
    if (declaration.name) str_print("", declaration.name);
    printf(" ");
    declaration_type_print(declaration.type);
    printf(" ");
    if (declaration.value) expression_print(*declaration.value);
    printf(" ");
    if (declaration.code) statement_print(*declaration.code);
    printf("\n");
    if (declaration.next) declaration_print(*declaration.next);
}

void declaration_type_print(const DeclarationType declaration_type) {
    printf("%s", DECLARATION_T_NAMES[declaration_type]);
}

void statement_print(const Statement statement) {
    printf("[S]: ");
    if (statement.declaration) declaration_print(*statement.declaration);
    printf(" ");
    if (statement.init_expression) expression_print(*statement.init_expression);
    printf(" ");
    if (statement.expression) expression_print(*statement.expression);
    printf(" ");
    if (statement.next_expression) expression_print(*statement.next_expression);
    printf(" ");
    if (statement.body) statement_print(*statement.body);
    printf(" ");
    if (statement.else_body) statement_print(*statement.else_body);
    printf("\n");
    if (statement.next) statement_print(*statement.next);
}

void statement_type_print(const StatementType statement_type) {
    printf("%s", STATEMENT_T_NAMES[statement_type]);
}

void expression_print(const Expression expression) {
    printf("[E]: ");
    if (expression.left) expression_print(*expression.left);
    printf(" ");
    if (expression.right) expression_print(*expression.right);
    printf(" ");
    if (expression.value) str_print("", expression.value);
    printf("\n");
}

void expression_type_print(const ExpressionType expression_type) {
    printf("%s", EXPRESSION_T_NAMES[expression_type]);
}

DeclarationType token_to_declaration_type(Token t) {
    switch (t) {
        case (KW_DECL): return DECLARATION_T_FUNCTION;
        case (KW_OPT):
        case (KW_VOID):
        case (KW_BYTE):
        case (KW_STRING):
        case (KW_U8):
        case (KW_U16):
        case (KW_U32):
        case (KW_U64):
        case (KW_I8):
        case (KW_I16):
        case (KW_I32):
        case (KW_I64):
        case (KW_F32):
        case (KW_F64):
        case (KW_BOOL): return DECLARATION_T_VARIABLE;
        default: return DECLARATION_T_UNKNOWN;
    }
}
