#ifndef __SYMBOL_H
#define __SYMBOL_H

#include "debug.h"
#include "str.h"
#include "token.h"

typedef struct {
    CharacterLocation location;
    Token t;
    str* s;
} Symbol;

Symbol* sym_new(const str* const s);
void _sym_free(Symbol*);
#define sym_free(s)                                                          \
do {                                                                         \
    _sym_free(s);                                                            \
    s = NULL;                                                                \
} while (0)

Symbol* sym_copy(const Symbol* s);
bool sym_cmp(const Symbol s1, const Symbol s2);
bool symbol_valid(const Symbol sym);
void sym_print(const Symbol sym);

bool sym_is_built_in_type(const Symbol sym);

#endif