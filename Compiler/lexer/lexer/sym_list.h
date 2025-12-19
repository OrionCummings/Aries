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

/// @brief Addds `sym` to the given symbol list. This function creates a new symbol (and str!) such that it does not take ownership of `sym`.
/// @param sl The symbol list in which to add `sym`.
/// @param sym The symbol to be added.
void sym_list_add(SymbolList* sl, Symbol sym);

bool symlist_valid(const SymbolList* const symlist);

void sym_list_print(const SymbolList sl);

#endif