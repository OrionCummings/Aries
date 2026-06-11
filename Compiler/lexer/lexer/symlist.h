#ifndef __symlist_H
#define __symlist_H

#include "symbol.h"

typedef struct {

    // The base index (used by the parser).
    index_t base_index;

    // The maximum capacity of the symbol list
    size_t capacity;

    // The current number of elements in the symbol list
    size_t length;

    // The symbols in the symbol list
    Symbol* symbols;
} symlist;

typedef enum : uint8_t {
    SYMLIST_INVALID = 0,
    SYMLIST_END,
    SYMLIST_SUCCESS,
} symlist_result_type;

typedef struct {
    symlist_result_type type;
    union {
        Symbol sym;
    } data;
} symlist_result;

symlist* symlist_new(const size_t capacity);
void _symlist_free(symlist* sl);
#define symlist_free(sl)   \
    do {                   \
        _symlist_free(sl); \
        sl = NULL;         \
    } while (0)

/// @brief Adds `sym` to the given symbol list. This function creates a new symbol (and str!) such that it does not
/// take ownership of `sym`.
/// @param sl The symbol list in which to add `sym`.
/// @param sym The symbol to be added.
///
/// TODO: Make this return `symlist_result`
void symlist_push(symlist* sl, Symbol sym);

/// @brief Returns the next symbol in the symlist and increments the index pointer by one.
/// @param sl The symbol list from which to `pop`.
/// @return The next symbol in the symlist (as wrapped by `symlist_result`)
symlist_result symlist_pop(symlist* const sl);

/// @brief Returns the next symbol in the symlist but does not increment the base index pointer (like `symlist_pop`).
/// @param sl The symbol list from which to `peek`.
/// @param offset The offset from the base index. N => peek at `base_index + N`
/// @return The next symbol in the symlist (as wrapped by `symlist_result`)
symlist_result symlist_peek(const symlist* const sl, index_t offset);

bool symlist_valid(const symlist* const symlist);

void symlist_print(const symlist sl);

#endif