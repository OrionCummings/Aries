#ifndef __SYM_LIST_H
#define __SYM_LIST_H

#include "symbol.h"

#define SYM_LIST_DEFAULT_SIZE ((size_t)64)

typedef struct {
    size_t capacity;
    size_t length;
    Symbol* symbols;
} SymbolList;

SymbolList* sym_list_new(const size_t capacity);
void _sym_list_free(SymbolList* sl);
#define sym_list_free(sl)                                                    \
do {                                                                         \
    _sym_list_free(sl);                                                      \
    sl = NULL;                                                               \
} while (0)

void sym_list_add(SymbolList* sl, Symbol* sym);

#endif