#include "token.h"

Token str_to_token(const str* const s) {
    if (s == NULL || s->data == NULL) {
        return INVALID;
    }

    for (size_t index = 3; index < TOKEN_COUNT; index++) {
        if (str_cmp_raw(s, SYM_CHARS[index])) {
            return (Token)index;
        }
    }

    if (str_is_identifier(s)) {
        return IDENTIFIER;
    }

    return str_is_literal(s);
}

