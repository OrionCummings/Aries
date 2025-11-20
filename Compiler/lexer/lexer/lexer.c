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
        if (sym == NULL) {
            A_WARNING("failed to create symbol");
            str_free(s);
            free(boundaries);
            return false;
        }
        sym->location = (CharacterRange){ .line = line, .char_start = char_start, .char_stop = char_start + char_len };

        char_start += char_len;
        if (sym->t == SYM_NEWLINE) {
            line++;
            char_start = 0;
        }

        lex_add_symbol(lexer, *sym);

        sym_free(sym);
        str_free(s);

        printf("");
    }

    free(boundaries);

    A_INFO("performed lexing");

    return true;
}

Lexer* lex_new(const char* filename) {

    arena* arena = arena_new(64 * sizeof(Symbol));
    if (arena == NULL) {
        A_ERROR("failed to create a new arena");
        arena_free(arena);
        return NULL;
    }
    A_INFO("created a new arena");

    // The file content lives in the arena
    str* file_content = astr_from_filename(arena, filename);
    if (file_content == NULL) {
        A_ERROR("failed to read file '%s'", filename);
        arena_free(arena);
        return NULL;
    }
    A_INFO("extracted file contents from '%s'", filename);

    // TODO: Is this strange? Is that bad?? Is this good??????
    // The lexer lives in the arena
    Lexer* lexer = arena_alloc(arena, sizeof(*lexer));
    if (lexer == NULL) {
        A_ERROR("failed to allocate new lexer");
        arena_free(arena);
        return NULL;
    }
    A_INFO("created a new lexer");

    // The symlist DOES NOT live in the arena because it must exist 
    // after the lexer is destroyed. The lifetime of the symlist is 
    // LONGER than that of the lexer.
    SymbolList* sym_list = sym_list_new(SYM_LIST_DEFAULT_SIZE);
    if (sym_list == NULL) {
        A_ERROR("failed to allocate new symbol list");
        arena_free(arena);
        return NULL;
    }
    A_INFO("created a new symlist");

    lexer->arena = arena;
    lexer->file_content = file_content;
    lexer->sym_list = sym_list;

    return lexer;
}

void _lex_free(Lexer* l) {
    if (l == NULL) { return; }
    arena_free(l->arena);
}

// TODO: sym could be const?
bool lex_add_symbol(Lexer* const lex, const Symbol const sym) {
    if (lex == NULL || lex->sym_list == NULL) { return false; }

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
