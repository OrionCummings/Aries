#include "lexer.h"

symlist* lex(const str const* file_content) {

    if (file_content == NULL) {
        A_WARNING("passed null parameter 'file_content'");
        return false;
    }

    symlist* symlist = symlist_new(8); // TODO: Magic number
    if (symlist == NULL) {
        A_ERROR("failed to create symlist"); // TODO: Refactor with goto cleanup
        return NULL;
    }
    A_INFO("created symlist");

    size_t file_len = str_len(file_content);
    if (file_len == 0) {
        A_WARNING("empty file provided");
        return symlist;
    }

    index_t* boundaries = str_get_alphanumeric_symbolic_boundaries(file_content);

    if (boundaries == NULL) {
        A_ERROR("Failed to create alphanumeric symbolic boundaires");
        symlist_free(symlist);
        return NULL;
    }

    size_t index = 0;
    uint16_t line = 1;
    size_t char_start = 0;
    while (boundaries[index++] != file_len) {

        // Get the relavent boundaries in the file contents
        index_t start = boundaries[index - 1];
        index_t end = boundaries[index];
        size_t char_len = end - start;

        // Get a view of the content within those boundaries
        str s = str_view(file_content, start, end);
        if (s.data == NULL) {
            A_ERROR("failed to create view");
            return false;
        }

        // Create a new symbol from the given string view
        Symbol* sym = sym_new(&s);
        if (sym == NULL) {
            A_WARNING("failed to create symbol");
            free(boundaries);
            return false;
        }

        // TODO: There is something wrong with this approach; many character
        // numbers are too high! Update the current line count
        char_start += char_len;
        if (sym->t == SYM_NEWLINE) {
            line++;
            char_start = 0;
        }

        // Update the symbol's location
        sym->location = crange(line, char_start, char_start + char_len);

        // If the previous symbol was a space and the current symbol is a space,
        // then don't add it to the sym list!
        if (sym->t != SYM_SPACE) {
            symlist_push(symlist, *sym);
        }

        // Free the symbol because it's no longer needed
        sym_free(sym);
    }

    free(boundaries);

    A_INFO("performed lexing");

    return symlist;
}

TokenType str_is_literal(const str* const s) {

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

    return TOKEN_INVALID;
}
