#ifndef __LEXER_H
#define __LEXER_H

#include <ctype.h>
#include <stddef.h>
#include "debug.h"
#include "sym_list.h"

typedef struct {
    str* file_content; // TODO: Should the lexer even have this?
    size_t index;
    SymbolList* sym_list;
} Lexer;

/// @brief Creates a new lexer object.
/// @param file_contents A pointer to a str object that contains a file to be lexed. The lexer takes ownership of this str object!
/// @return A pointer to a new lexer object. Returns NULL on failure.
Lexer* lex_new(str* file_contents);

void _lex_free(Lexer* lexer);
#define lex_free(l) \
do {                \
    _lex_free(l);   \
    l = NULL;       \
} while (0)

bool lex(Lexer* lexer);
bool lex_add_symbol(Lexer* const lex, const Symbol* const sym);
Token lex_buffer_to_token(char token_buffer[MAX_IDENTIFIER_LENGTH]);
void lex_print(const Lexer* const lexer);

#endif
