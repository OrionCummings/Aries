#ifndef __LEXER_H
#define __LEXER_H

#include <ctype.h>
#include <stddef.h>
#include "debug.h"
#include "sym_list.h"

typedef struct {
    arena* arena; // TODO: Should this have a more specific scope? (symbols/strings?)
    str* file_content; // TODO: Should the lexer even own this?
    size_t index;
    SymbolList* sym_list;
} Lexer;

SymbolList* lex(const str* file_content);
void lex_print(const Lexer* const lexer); 

#endif
