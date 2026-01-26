#ifndef __symlist_H
#define __symlist_H

#include "symbol.h"

// TODO: Magic number!
#define symlist_DEFAULT_SIZE ((size_t)64)

typedef struct {

    // The base index (used by the parser).
    index_t base_index;

    // The lookahead index (used by the parser).
    index_t la_index;

    // The maximum capacity of the symbol list
    size_t capacity;

    // The current number of elements in the symbol list
    size_t length;

    // The symbols in the symbol list
    Symbol* symbols;
} SymbolList;

SymbolList* symlist_new(const size_t capacity);
void _symlist_free(SymbolList* sl);
#define symlist_free(sl)                                                    \
do {                                                                         \
    _symlist_free(sl);                                                      \
    sl = NULL;                                                               \
} while (0)

/// @brief Addds `sym` to the given symbol list. This function creates a new symbol (and str!) such that it does not take ownership of `sym`.
/// @param sl The symbol list in which to add `sym`.
/// @param sym The symbol to be added.
void symlist_add(SymbolList* sl, Symbol sym);

bool symlist_valid(const SymbolList* const symlist);

void symlist_print(const SymbolList sl);

#endif