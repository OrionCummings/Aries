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

Declaration* parse_parameter_list(arena* arena, symlist* symlist, const index_t max_params) {
    if (arena == NULL) {
        A_WARNING("bad parameter 'arena'");
        return NULL;
    }

    if (symlist == NULL) {
        A_WARNING("bad parameter 'symlist'");
        return NULL;
    }

    if (max_params == 0) {
        A_WARNING("bad parameter 'max_params'");
        return NULL;
    }

    Declaration* decl = arena_alloc(arena, sizeof(*decl));
    if (decl == NULL) {
        A_WARNING("failed to allocate declaration");
        return NULL;
    }

    Declaration* decl_active = decl;

    symlist_result open_paren_res = symlist_peek(symlist, 0);
    if (open_paren_res.type != SYMLIST_SUCCESS) {
        A_WARNING("failed to peek symlist");
        return NULL;
    }
    Symbol open_paren = open_paren_res.data.sym;

    if (open_paren.t != SYM_PAREN_OPEN) {
        A_WARNING("expected function parameter list to start with open paren");
        return NULL;
    }

    // Pop the open paren
    (void)symlist_pop(symlist);

    bool more_params = true;
    index_t param_index = 0;
    while ((param_index < max_params) && more_params) {
        decl_active->decl_type = DT_PARAMETER;

        symlist_result a_res = symlist_peek(symlist, 0);
        if (a_res.type != SYMLIST_SUCCESS) {
            A_WARNING("failed to peek symlist");
            return NULL;
        }
        Symbol a = a_res.data.sym;
        (void)symlist_pop(symlist);

        if (a.t == SYM_PAREN_CLOSE) {
            break;
        }

        if (str_is_identifier(a.s)) {
            decl_active->type = a.s;
        }

        symlist_result b_res = symlist_peek(symlist, 0);
        if (b_res.type != SYMLIST_SUCCESS) {
            A_WARNING("failed to peek symlist");
            return NULL;
        }
        Symbol b = b_res.data.sym;
        (void)symlist_pop(symlist);

        if (str_is_identifier(b.s)) {
            decl_active->name = b.s;
        }

        symlist_result c_res = symlist_peek(symlist, 0);
        if (c_res.type != SYMLIST_SUCCESS) {
            A_WARNING("failed to peek symlist");
            return NULL;
        }
        Symbol c = c_res.data.sym;

        if (c.t != SYM_COMMA) {
            more_params = false;
        } else {
            (void)symlist_pop(symlist); // pop the comma

            Declaration* decl_next = arena_alloc(arena, sizeof(*decl_next));
            if (decl_next == NULL) {
                A_WARNING("failed to allocate decl_next");
                return NULL;
            }

            decl_active->next = decl_next;

            decl_active = decl_next;
        }

        ++param_index;
    }

    if (param_index == max_params) {
        A_ERROR("attempted to parse more that the max number of parameters");
        return NULL;
    }

    symlist_result close_paren_res = symlist_peek(symlist, 0);
    if (close_paren_res.type != SYMLIST_SUCCESS) {
        A_WARNING("failed to peek symlist");
        return NULL;
    }
    Symbol close_paren = close_paren_res.data.sym;

    if (close_paren.t != SYM_PAREN_CLOSE) {
        A_WARNING("expected function parameter list to end with close paren");
        return NULL;
    }

    // Pop the close paren
    (void)symlist_pop(symlist);

    return decl;
}

Declaration* declaration_parse(arena* arena, symlist* const symlist) {

    if (arena == NULL) {
        A_ERROR("passed null arena");
        return NULL;
    }

    if (symlist == NULL) {
        A_ERROR("passed null symlist");
        return NULL;
    }

    Declaration* decl = arena_alloc(arena, sizeof(*decl));
    if (!decl) {
        A_WARNING("failed to allocate from arena");
        return NULL;
    }

    symlist_result next_decl_res = symlist_peek(symlist, 0);
    if (next_decl_res.type != SYMLIST_SUCCESS) {
        A_WARNING("failed to peek symlist");
        return NULL;
    }
    Symbol next_decl = next_decl_res.data.sym;
    (void)symlist_pop(symlist);

    if (next_decl.t == KW_DECL) {
        decl->decl_type = DT_FUNCTION; // update the decl type
        symlist_result next_name_res = symlist_peek(symlist, 0);
        if (next_name_res.type != SYMLIST_SUCCESS) {
            A_WARNING("failed to peek symlist");
            return NULL;
        }
        Symbol next_name = next_name_res.data.sym;
        (void)symlist_pop(symlist); // pop the function name

        decl->name = next_name.s; // update the decl name
        decl->parameters = parse_parameter_list(arena, symlist, 64);

        bool found_arrow = false;
        while (!found_arrow) {
            symlist_result next_dash_res = symlist_peek(symlist, 0);
            symlist_result next_gt_res = symlist_peek(symlist, 1);
            if (next_dash_res.type != SYMLIST_SUCCESS || next_gt_res.type != SYMLIST_SUCCESS) {
                A_WARNING("failed to peek symlist");
                return NULL;
            }
            Symbol next_dash = next_dash_res.data.sym;
            Symbol next_gt = next_gt_res.data.sym;
            found_arrow = str_cmp_raw(next_dash.s, "-") && str_cmp_raw(next_gt.s, ">");

            (void)symlist_pop(symlist);
            (void)symlist_pop(symlist);
        }
        symlist_result next_return_type_res = symlist_peek(symlist, 0);
        if (next_return_type_res.type != SYMLIST_SUCCESS) {
            A_WARNING("failed to peek symlist");
            return NULL;
        }
        Symbol next_return_type = next_return_type_res.data.sym;
        // TODO: Check if it's a type!
        decl->return_type = next_return_type.s;
    } else {
        A_WARNING("not a function decl");
    }

    return decl;
}

// TODO: Add more error checking; temp function probably lol
Declaration* declaration_new(arena* arena) {
    Declaration* decl = arena_alloc(arena, sizeof(*decl));
    return decl;
}

bool declaration_eq(const Declaration* const a, const Declaration* const b) {
    if ((a == NULL) && (b == NULL)) {
        return true;
    }

    if ((a == NULL) ^ (b == NULL)) {
        return false;
    }

    bool decl_type = str_cmp(a->type, b->type);
    bool name_eq = str_cmp(a->name, b->name);
    bool return_type_eq = str_cmp(a->return_type, b->return_type);
    bool parameters_eq = declaration_eq(a->parameters, b->parameters);
    bool value_eq = expression_eq(a->value, b->value);
    bool next_eq = declaration_eq(a->next, b->next);

    return (decl_type && name_eq && return_type_eq && parameters_eq && value_eq && next_eq);
}

// TODO: Why is there expression_parse and expression_new?

Expression* expression_new(arena* arena, ExpressionType type, str* s) {
    if (arena == NULL) {
        A_WARNING("invalid arena");
        return NULL;
    }
    if ((type != ET_UNKNOWN) && (!str_valid(s))) {
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

Expression* expression_parse_pratt(arena* arena, symlist* const symlist) {
    Expression* lhs = expression_parse_pratt_primary(arena, symlist);
    return expression_parse_pratt_left(arena, symlist, 0, OPERATOR_PRECEDENCE_MIN, lhs);
}

Expression* expression_parse_pratt_primary(arena* arena, symlist* const symlist) { return NULL; }

Expression* expression_parse_pratt_left(arena* arena, symlist* const symlist, index_t index, precedence min_prec,
                                        Expression* lhs) {

    // Peek the next symbol
    symlist_result res_lookahead = symlist_peek(symlist, 0);
    if (res_lookahead.type != SYMLIST_SUCCESS) {
        if (res_lookahead.type == SYMLIST_INVALID) {
            A_WARNING("failed to get lookahead: invalid lookahead");
        }
        if (res_lookahead.type == SYMLIST_END) {
            A_WARNING("failed to get lookahead: end of symlist");
        }
        return NULL;
    }
    Symbol lookahead = res_lookahead.data.sym;

    precedence_result res_prec = sym_precedence(lookahead);
    if (res_prec.type != PREC_VALID) {
        A_WARNING("failed to get lookahead lookahead");
        return NULL;
    }

    bool is_binop = token_type_is_binop(res_lookahead.data.sym.t);
    bool is_greater_precedence = res_prec.prec >= min_prec;

    while (is_binop && is_greater_precedence) {
        Symbol op = res_lookahead.data.sym;
        symlist->base_index++; // Advance to the next symbol
        Expression* rhs = expression_parse_pratt_primary(arena, symlist);

        // Peek the next symbol
        symlist_result res_lookahead = symlist_peek(symlist, 0);
        if (res_lookahead.type != SYMLIST_SUCCESS) {
            if (res_lookahead.type == SYMLIST_INVALID) {
                A_WARNING("failed to get lookahead: invalid lookahead");
            }
            if (res_lookahead.type == SYMLIST_END) {
                A_WARNING("failed to get lookahead: end of symlist");
            }
            return NULL;
        }
        Symbol lookahead = res_lookahead.data.sym;

        precedence_result res_prec = sym_precedence(lookahead);
        if (res_prec.type != PREC_VALID) {
            A_WARNING("failed to get lookahead lookahead");
            return NULL;
        }

        bool is_binop = token_type_is_binop(res_lookahead.data.sym.t);
        bool is_greater_precedence = res_prec.prec >= min_prec;
        // bool is_equal_precedence = x == res_prec.prec;
        // while ((is_binop && is_greater_precedence) || (is_right_associative_op() && is_equal_precedence)) {
        //     rhs = expression_parse_pratt_left();
        // }
    }

    return lhs;
}

// TODO: Do we need an index?
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

    A_WARNING("UNFINISHED FUNCTION");
    return NULL;

    // Expression* e = expression_new(arena, ET_UNKNOWN, NULL);

    // symlist_result res_lookahead = symlist_peek(symlist, 0);
    // switch (res_lookahead.type) {
    // case (SYMLIST_INVALID): {
    //     A_WARNING("failed to get lookahead: invalid lookahead");
    //     return NULL;
    // }
    // case (SYMLIST_END): {
    //     A_WARNING("failed to get lookahead: end of symlist");
    //     return NULL;
    // }
    // case (SYMLIST_SUCCESS): {
    // }
    // }

    // Symbol lookahead = res_lookahead.data.sym;
    // bool is_binop = token_type_is_binop(lookahead.t);
    // precedence_result lookahead_prec_res = sym_precedence(lookahead);
    // if (lookahead_prec_res.type != PREC_VALID) {
    //     A_WARNING("failed to get lookahead precedence");
    //     return;
    // }

    // precedence prec = lookahead_prec_res.prec;

    // while (is_binop && (prec >= OPERATOR_PRECEDENCE_MIN)) {
    // }

    // return e;
}

void declaration_print(const Declaration declaration) {
    printf("{ decl_type = ");
    declaration_type_print(declaration.decl_type);
    printf(", ");

    if (declaration.type) {
        str_print("type = ", declaration.type);
    } else {
        printf("<null>");
    }
    printf(", ");

    if (declaration.name) {
        str_print("name = ", declaration.name);
    } else {
        printf("<null>");
    }
    printf(", ");

    if (declaration.return_type) {
        str_print("return_type = ", declaration.return_type);
    } else {
        printf("<null>");
    }
    printf(", ");

    if (declaration.parameters) {
        declaration_print(*declaration.parameters);
    } else {
        printf("<null>");
    }
    printf(", ");

    if (declaration.value) {
        expression_print(*declaration.value, 0);
    } else {
        printf("<null>");
    }
    printf(", ");

    if (declaration.next) {
        declaration_print(*declaration.next);
    } else {
        printf("<null>");
    }
    printf(" }");
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

Statement* statement_new(arena* arena) { return arena_alloc(arena, sizeof(Statement)); }

Statement* statement_parse(arena* arena, symlist* const symlist) {
    A_WARNING("not implemented!");
    return NULL;
}

bool statement_eq(const Statement* const a, const Statement* const b) {
    if ((a == NULL) && (b == NULL)) {
        return true;
    }

    if ((a == NULL) ^ (b == NULL)) {
        return false;
    }

    bool eq_type = a->type == b->type;
    bool eq_declaration = declaration_eq(a->declaration, b->declaration);
    bool eq_else_body = statement_eq(a->else_body, b->else_body);
    bool eq_expression = expression_eq(a->expression, b->expression);
    bool eq_init_expression = expression_eq(a->init_expression, b->init_expression);
    bool eq_next = statement_eq(a->next, b->next);
    bool eq_next_expression = expression_eq(a->next_expression, b->next_expression);

    return eq_type && eq_declaration && eq_else_body && eq_expression && eq_init_expression && eq_next;
}

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
