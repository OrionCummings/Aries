#include "lexer.h"

bool lex(Lexer* lexer) {

    if (lexer == NULL) {
        A_WARNING("passed null parameter 'lexer'");
        return false;
    }

    size_t len = str_len(lexer->file_content);
    index_t* boundaries = str_get_alphanumeric_symbolic_boundaries(lexer->file_content);

    size_t index = 0;
    uint16_t line = 1;
    size_t char_start = 0;
    char buffer[MAX_IDENTIFIER_LENGTH];
    while (boundaries[index++] != len) {

        // Clear the char buffer
        memset(buffer, 0, MAX_IDENTIFIER_LENGTH);

        index_t start = boundaries[index - 1];
        index_t end = boundaries[index];

        size_t char_len = end - start;

        str* s = str_copy(lexer->file_content, start, end);
        if (s == NULL) {
            A_WARNING("failed to copy string");
            return false;
        }

        Symbol* sym = sym_new(s);
        sym->location = (CharacterRange){ .line = line, .char_start = char_start, .char_stop = char_start + char_len };

        if (sym == NULL) {
            A_WARNING("failed to create symbol");
            return false;
        }

        char_start += char_len;
        if (sym->t == SYM_NEWLINE) {
            line++;
            char_start = 0;
        }

        lex_add_symbol(lexer, sym);
        // sym_print(*sym);

        str_free(s);     // Freeing these breaks the lexer!
        // sym_free(sym);   // AHHHHHHHHHHHHHH
    }

    free(boundaries);

    return true;
}

Lexer* lex_new(str* file_contents) {

    Lexer* lexer = calloc(1, sizeof(*lexer));
    if (lexer == NULL) {
        A_WARNING("failed to allocate new lexer");
        return NULL;
    }

    void* temp = sym_list_new(SYM_LIST_DEFAULT_SIZE);
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
    if (l != NULL) {
        str_free(l->file_content);
        sym_list_free(l->sym_list);
    }
    free(l);
}

// TODO: sym could be const?
bool lex_add_symbol(Lexer* const lex, const Symbol* const sym) {
    if (lex == NULL || lex->sym_list == NULL || sym == NULL) { return false; }

    sym_list_add(lex->sym_list, sym);

    return true;
}

void lex_print(const Lexer* const lexer) {
    printf("Lexer ");

    if (lexer == NULL) {
        printf("\t<null>\n");
        return;
    }

    
    if (lexer->sym_list != NULL) {
        printf("(%lu/%lu):\n", lexer->sym_list->length, lexer->sym_list->capacity);
        sym_list_print(*lexer->sym_list);
    }
    printf("\n");
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
