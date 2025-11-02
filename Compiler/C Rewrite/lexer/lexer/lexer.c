#include "lexer.h"

bool lex(Lexer* lexer) {

    if (lexer == NULL) {
        A_WARNING("Passed null parameter 'lexer'");
        return false;
    }

    size_t len = str_len(lexer->file_content);
    index_t* boundaries = str_get_alphanumeric_symbolic_boundaries(lexer->file_content);

    size_t index = 0;
    uint16_t line = 1;
    char buffer[MAX_IDENTIFIER_LENGTH];
    while (boundaries[index++] != len) {

        // Clear the char buffer
        memset(buffer, 0, MAX_IDENTIFIER_LENGTH);

        index_t start = boundaries[index - 1];
        index_t end = boundaries[index];

        str* s = str_copy(lexer->file_content, start, end);
        if (s == NULL) {
            A_WARNING("Failed to copy string");
            return false;
        }

        Symbol* sym = sym_new(s);
        sym->location = (CharacterRange){ .line = line, .char_start = start, .char_stop = end };
        if (sym->t == SYM_NEWLINE) {
            line++;
        }

        if (sym == NULL) {
            A_WARNING("Failed to create symbol");
            return false;
        }

        lex_add_symbol(lexer, sym);
        sym_print(*sym);
    }

    free(boundaries);

    return true;
}

Lexer* lex_new(size_t capacity, const str* file_contents) {

    Lexer* lexer = calloc(1, sizeof(*lexer));
    if (lexer == NULL) {
        A_WARNING("failed to allocate new lexer");
        return NULL;
    }

    void* temp = sym_list_new(capacity);
    if (temp == NULL) {
        A_WARNING("failed to allocate new symbol list");
        lex_free(lexer);
        return NULL;
    }
    lexer->sym_list = temp;
    lexer->file_content = file_contents;

    return lexer;
}

// TODO: I'm not convinved that this is correct; add some tests
void _lex_free(Lexer* l) {
    if (l == NULL) {
        return;
    }
    // fclose(l->file);
    // for (size_t index = 0; index < l->symbol_length; index++){
    //     sym_free(l->symbols[index]);
    // }
    // free(l->symbols);
    // free(l);
}

bool lex_add_symbol(Lexer* const lex, Symbol* sym) {
    if (lex == NULL || lex->sym_list == NULL) { return false; }

    sym_list_add(lex->sym_list, sym);

    return true;
}

Token str_is_literal(const str* const s) {

    // TODO: Play with the order to get the correct precedence!
    // TODO: Add ALL literals!!!!
    if (str_is_bool_literal(s)) {
        return LIT_BOOL;
    } else if (str_is_u8_literal(s)) {
        return LIT_U8;
    } else if (str_is_u16_literal(s)) {
        return LIT_U16;
    } else if (str_is_u32_literal(s)) {
        return LIT_U32;
    } else if (str_is_u64_literal(s)) {
        return LIT_U64;
    } else if (str_is_i8_literal(s)) {
        return LIT_I8;
    } else if (str_is_i16_literal(s)) {
        return LIT_I16;
    } else if (str_is_i32_literal(s)) {
        return LIT_I32;
    } else if (str_is_i64_literal(s)) {
        return LIT_I64;
    }

    return INVALID;
}
