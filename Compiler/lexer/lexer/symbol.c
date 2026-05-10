#include "symbol.h"

/// @brief Create a new symbol. This function makes a copy of the given pointer
/// and therefore does not take ownership of it.
/// @param s The string on which to base the new symbol.
/// @return A pointer to the new symbol. NULL on failure.
Symbol* sym_new(const str* const s) {

    if (s == NULL) {
        return NULL;
    }

    Symbol* sym = calloc(1, sizeof(Symbol));
    if (sym == NULL) {
        A_WARNING("failed to allocate new symbol");
        return NULL;
    }

    sym->t = str_to_token(s);
    if (sym->t == TOKEN_INVALID) {
        sym_free(sym);
        return NULL;
    }

    str* new_str = str_copy(s, 0, s->length);
    if (new_str == NULL) {
        sym_free(sym);
        return NULL;
    }
    sym->s = new_str;

    return sym;
}

void _sym_free(Symbol* s) {
    if (s != NULL) {
        str_free(s->s);
    }
    free(s);
}

Symbol* sym_copy(const Symbol* s) {
    if (s == NULL) {
        A_WARNING("attempted to copy null symbol");
        return NULL;
    }
    str* copy_str = str_copy(s->s, 0, str_len(s->s));
    Symbol* sym = sym_new(copy_str);
    if (sym == NULL) {
        A_WARNING("failed to copy symbol");
        return NULL;
    }

    sym->location = s->location;
    sym->t = s->t;

    return sym;
}

bool sym_cmp(const Symbol s1, const Symbol s2) {
    return (s1.t == s2.t && str_cmp(s1.s, s2.s));
}

bool sym_valid(const Symbol sym) {
    if (sym.t == TOKEN_INVALID) {
        return false;
    }
    if (sym.location.start == sym.location.end) {
        return false;
    }
    if (!str_valid(sym.s)) {
        return false;
    }
    return true;
}

void sym_print(const Symbol s) {
    printf("[%s:%d(%d-%d)]: ", TOKEN_NAMES[s.t], s.location.line,
           s.location.start, s.location.end);
    if (s.t == SYM_NEWLINE) {
        printf("'\\n'\n");
    } else {
        printf("'%.*s'\n", (int)s.s->length, s.s->data);
    }
}

bool sym_is_built_in_type(const Symbol sym) {
    TokenType t = sym.t;
    return ((t == KW_OPT) || (t == KW_VOID) || (t == KW_BYTE)
            || (t == KW_STRING) || (t == KW_U8) || (t == KW_U16)
            || (t == KW_U32) || (t == KW_U64) || (t == KW_I8) || (t == KW_I16)
            || (t == KW_I32) || (t == KW_I64) || (t == KW_F32) || (t == KW_F64)
            || (t == KW_BOOL));
}