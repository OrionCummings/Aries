#include "parser.h"

Declaration* parse(arena* arena, symlist* const symlist) {

    // TODO: This is a rather inefficient check but I think it's safe for now.
    // Reevaluate later!
    if (!symlist_valid(symlist)) {
        A_ERROR("cannot parse an invalid symlist");
        return NULL;
    }

    return declaration_parse(arena, symlist); // NOTE: This is correct, but not for current testing!
}

Declaration* declaration_parse(arena* arena, symlist* const symlist) {

    // TODO: Add some bounds checking to the symlist base and look-ahead
    // indices.

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
        if (type == DT_UNKNOWN) {
            A_WARNING("failed to convert token to declaration type");
            return NULL;
        }
        declaration->type = type;

        // TODO: Should we accept non-initialized variables?
        // Example: "u32 x;" <-- should this be acceptable? Methinks not.

        symlist->base_index += 3; // Skip ahead 3 symbols (<type> <name> <symbol> <expression>)
        Expression* value = expression_parse(arena, symlist, symlist->base_index);
        if (!value) {
            A_WARNING("failed to parse expressionession");
            return NULL;
        }
        declaration->value = value;

        return declaration;
    }

    return NULL;
}

// TODO: Why is there expression_parse and expression_new?

Expression* expression_new(arena* arena, ExpressionType type, str* s) {
    if (arena == NULL) {
        A_WARNING("invalid arena");
        return NULL;
    }
    if (!str_valid(s)) {
        A_WARNING("invalid string");
        return NULL;
    }

    Expression* expr = NULL;

    void* mem = arena_alloc(arena, sizeof(*expr));
    if (mem == NULL) {
        A_WARNING("failed to allocate new expression!");
        return expr;
    }

    expr = mem;
    expr->type = type;
    expr->value = s;
    expr->left = nullptr;
    expr->right = nullptr;

    return expr;
}

Expression* expression_parse(arena* arena, symlist* const symlist, index_t index) {
    if (arena == NULL) {
        A_WARNING("invalid arena");
        return NULL;
    }
    if (symlist == NULL) {
        A_WARNING("invalid symlist");
        return NULL;
    }
    if (symlist->symbols == NULL) {
        A_WARNING("invalid symlist->symbols");
        return NULL;
    }
    if (symlist->length < index) {
        A_WARNING("index too large");
        return NULL;
    }

    Expression* e = arena_alloc(arena, sizeof(*e));

    symlist_result res_a = symlist_peek(symlist, 0);  // 'A' + B
    symlist_result res_op = symlist_peek(symlist, 1); // A '+' B
    symlist_result res_b = symlist_peek(symlist, 2);  // A + 'B'

    if (res_a.type == SYMLIST_SUCCESS) {
        Symbol sym_a = res_a.data.sym;

        if ((res_op.type == SYMLIST_SUCCESS) && (res_b.type == SYMLIST_SUCCESS)) {
            Symbol sym_op = res_op.data.sym;
            Symbol sym_b = res_b.data.sym;

            if (token_type_is_binop(sym_op.t) && (sym_a.t == sym_b.t)) {

                Expression* expr_left = expression_new(arena, ET_LIT_U8, sym_a.s);
                Expression* expr_right = expression_new(arena, ET_LIT_U8, sym_b.s);

                e->type = ET_BIN_OP_ADD; // TODO: Make this more general; binop =/> OP_ADD
                e->left = expr_left;
                e->right = expr_right;
                e->value = nullptr;
            }
            // TODO: These str functions should be implemented on symbols instead. Decouple from str_lib.
        } else if (str_is_u8_literal(sym_a.s)) {
            e->type = ET_LIT_U8;
            e->value = sym_a.s;
            e->left = nullptr; // TODO: this may not be necessary? calloc/arenas are zero-initialized?
            e->right = nullptr;
        } else if (str_is_u16_literal(sym_a.s)) {
            e->type = ET_LIT_U16;
            e->value = sym_a.s;
            e->left = nullptr;
            e->right = nullptr;
        } else if (str_is_u32_literal(sym_a.s)) {
            e->type = ET_LIT_U32;
            e->value = sym_a.s;
            e->left = nullptr;
            e->right = nullptr;
        } else if (str_is_u64_literal(sym_a.s)) {
            e->type = ET_LIT_U64;
            e->value = sym_a.s;
            e->left = nullptr;
            e->right = nullptr;
        }

    } else {
        // TODO: Make this more robust!
        A_WARNING("failed to parse expression");
        return NULL;
    }

    return e;
}

// bool valid_start_expression(TokenType t) { return (t ==); }

void declaration_print(const Declaration declaration) {
    printf("[D]: ");
    if (declaration.name)
        str_print("", declaration.name);
    printf(" ");
    declaration_type_print(declaration.type);
    printf(" ");
    if (declaration.value)
        expression_print(*declaration.value, 0);
    printf(" ");
    if (declaration.code)
        statement_print(*declaration.code);
    printf("\n");
    if (declaration.next)
        declaration_print(*declaration.next);
}

void declaration_type_print(const DeclarationType declaration_type) { printf("%s", DT_NAMES[declaration_type]); }

void statement_print(const Statement statement) {
    printf("[S]: ");
    if (statement.declaration)
        declaration_print(*statement.declaration);
    printf(" ");
    if (statement.init_expression)
        expression_print(*statement.init_expression, 0);
    printf(" ");
    if (statement.expression)
        expression_print(*statement.expression, 0);
    printf(" ");
    if (statement.next_expression)
        expression_print(*statement.next_expression, 0);
    printf(" ");
    if (statement.body)
        statement_print(*statement.body);
    printf(" ");
    if (statement.else_body)
        statement_print(*statement.else_body);
    printf("\n");
    if (statement.next)
        statement_print(*statement.next);
}

void statement_type_print(const StatementType statement_type) { printf("%s", ST_NAMES[statement_type]); }

bool expression_eq(const Expression* const e1, const Expression* const e2) {

    // TODO: Surely this logic could be simplified.
    bool s0 = (e1 == NULL) && (e2 == NULL);
    if (s0) {
        return true;
    }

    bool s1 = (e1 == NULL) || (e2 == NULL);
    if (s1) {
        return false;
    }

    bool s2 = e1->type == e2->type;
    bool s3 = expression_eq(e1->left, e2->left);
    bool s4 = expression_eq(e1->right, e2->right);
    bool s5 = str_cmp(e1->value, e2->value);
    return s2 && s3 && s4 && s5;
}

void expression_print(const Expression expression, size_t depth) {

    // This padding method it a bit strange but I don't *expect* it to be
    // modified lol
    char* padding = calloc(depth + 2, sizeof(*padding));
    for (index_t i = 0; i < depth; i++)
        padding[i] = '\t';
    padding[depth] = '\0';
    padding[depth + 1] = '\0';

    printf("%s[E]: \n", padding);

    padding[depth] = '\t'; // 'extend' the string so subsequent padding is one unit longer

    printf("%stype:  ", padding);           // extra space b/c |'type'| < |'right'|
    expression_type_print(expression.type); // TODO/BUG: 35 is not a valid type!!!!!
    printf("\n");

    printf("%sleft:  ", padding); // extra space b/c |'left'| < |'right'|
    if (expression.left) {
        expression_print(*expression.left, depth + 1);
    } else {
        printf("<null>\n");
    }
    printf("%sright: ", padding);
    if (expression.right) {
        expression_print(*expression.right, depth + 1);
    } else {
        printf("<null>\n");
    }
    printf("%svalue: ", padding);
    if (expression.value) {
        str_print("", expression.value);
    } else {
        printf("<null>\n");
    }
    printf("\n");

    free(padding);
}

void expression_type_print(const ExpressionType expression_type) { printf("%s", ET_NAMES[expression_type]); }

DeclarationType token_to_declaration_type(TokenType t) {
    switch (t) {
    case (KW_DECL):
        return DT_FUNCTION;
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
    case (KW_BOOL):
        return DT_VARIABLE;
    default:
        return DT_UNKNOWN;
    }
}
