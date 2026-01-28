#include "parser.h"

Declaration* parse(arena* arena, SymbolList* const symlist) {

    // TODO: This is a rather inefficient check but I think it's safe for now. Reevaluate later!
    if (!symlist_valid(symlist)) {
        A_ERROR("cannot parse an invalid symlist");
        return NULL;
    }

    return decl_parse(arena, symlist); // NOTE: This is correct, but not for current testing!
}

Declaration* decl_parse(arena* arena, SymbolList* const symlist) {

    // TODO: Add some bounds checking to the symlist base and look-ahead indices.

    // while (symlist->length < symlist->capacity) { // TODO: This seems flawed!

    Declaration* decl = arena_alloc(arena, sizeof(*decl));

    if (!decl) {
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
            A_WARNING("failed to get decl name");
            return NULL;
        }
        decl->name = varname;

        DeclarationType type = token_to_decl_type(base_sym.t);
        if (type == DECL_T_UNKNOWN) {
            A_WARNING("failed to convert token to decl type");
            return NULL;
        }
        decl->type = type;

        // TODO: Should we accept non-initialized variables?
        // Example: "u32 x;" <-- should this be acceptable? Methinks not.

        symlist->base_index += 3; // Skip ahead 3 symbols (<type> <name> <symbol> <EXPR>)
        Expression* value = expr_parse(arena, symlist);
        if (!value) {
            A_WARNING("failed to parse expression");
            return NULL;
        }
        decl->value = value;

        return decl;
    }

    return NULL;
}

Expression* expr_parse(arena* arena, SymbolList* const symlist) {

    // TODO: Add some bounds checking to the symlist base and look-ahead indices.
    if (arena == NULL) { A_WARNING("invalid arena"); return NULL; }
    if (symlist == NULL) { A_WARNING("invalid symlist"); return NULL; }
    if (symlist->la_index > symlist->length) { A_WARNING("invalid symlist la index"); return NULL; }

    Expression* expr = arena_alloc(arena, sizeof(*expr));
    if (!expr) { A_WARNING("failed to allocate memory for an expression"); return NULL; }

    Symbol sym = symlist->symbols[symlist->base_index];
    if (!sym_valid(sym)) { A_WARNING("failed to get valid symbol"); return NULL; }

    sym_print(sym);

    switch (sym.t) {

        case(SYM_PAREN_OPEN): {

            // Increment the look ahead index!
            symlist->la_index++;
            Expression* e = expr_parse(arena, symlist);
            if (!e) { A_WARNING("failed to allocate memory for an expression"); return NULL; }

        }

        case(LIT_U8):
        case(LIT_U16):
        case(LIT_U32):
        case(LIT_U64): {
            uint64_t value = 0; // TODO: This *probably shouldn't* be a 64-bit int?
            bool success = str_to_integer_value(sym.s, &value);
            if (!success) {
                A_WARNING("failed to convert str to int value");
                return NULL;
            }

            expr->int_value = value;
            expr->type = EXPR_T_LIT_U8; // TODO: Make this actually work with other types LOL
        }
    }

    return expr;
}

void decl_print(const Declaration decl) {
    printf("[DECL]: ");
    if (decl.name) str_print("", decl.name);
    printf(" ");
    decl_type_print(decl.type);
    printf(" ");
    if (decl.value) expr_print(*decl.value);
    printf(" ");
    if (decl.code) stmt_print(*decl.code);
    printf("\n");
    if (decl.next) decl_print(*decl.next);
}

void decl_type_print(const DeclarationType decl_type) {
    printf("%s", DECL_T_NAMES[decl_type]);
}

void stmt_print(const Statement stmt) {
    printf("[STMT]: ");
    if (stmt.decl) decl_print(*stmt.decl);
    printf(" ");
    if (stmt.init_expr) expr_print(*stmt.init_expr);
    printf(" ");
    if (stmt.expr) expr_print(*stmt.expr);
    printf(" ");
    if (stmt.next_expr) expr_print(*stmt.next_expr);
    printf(" ");
    if (stmt.body) stmt_print(*stmt.body);
    printf(" ");
    if (stmt.else_body) stmt_print(*stmt.else_body);
    printf("\n");
    if (stmt.next) stmt_print(*stmt.next);
}

void stmt_type_print(const StatementType stmt_type) {
    printf("%s", STMT_T_NAMES[stmt_type]);
}

void expr_print(const Expression expr) {
    printf("[EXPR]: ");
    if (expr.left) expr_print(*expr.left);
    printf(" ");
    if (expr.right) expr_print(*expr.right);
    printf(" ");
    printf("%s%lu", (expr.negative) ? "-" : "", expr.int_value);
    if (expr.str_value) printf("%s", expr.str_value);
    printf("\n");
}

void expr_type_print(const ExpressionType expr_type) {
    printf("%s", EXPR_T_NAMES[expr_type]);
}

DeclarationType token_to_decl_type(Token t) {
    switch (t) {
        case (KEYWORD_DECL): return DECL_T_FUNCTION;
        case (KEYWORD_OPT):
        case (KEYWORD_VOID):
        case (KEYWORD_BYTE):
        case (KEYWORD_STRING):
        case (KEYWORD_U8):
        case (KEYWORD_U16):
        case (KEYWORD_U32):
        case (KEYWORD_U64):
        case (KEYWORD_I8):
        case (KEYWORD_I16):
        case (KEYWORD_I32):
        case (KEYWORD_I64):
        case (KEYWORD_F32):
        case (KEYWORD_F64):
        case (KEYWORD_BOOL): return DECL_T_VARIABLE;
        default: return DECL_T_UNKNOWN;
    }
}


