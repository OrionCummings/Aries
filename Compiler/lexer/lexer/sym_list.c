#include "sym_list.h"

SymbolList* sym_list_new(const size_t capacity) {
    SymbolList* sl = calloc(1, sizeof(*sl));

    if (sl == NULL) {
        A_WARNING("failed to allocate new sym list object");
        return NULL;
    }

    sl->capacity = capacity;
    sl->length = 0;
    sl->symbols = calloc(capacity, sizeof(*sl->symbols));

    if (sl->symbols == NULL) {
        A_WARNING("failed to allocate new symbol list in a sym list object");
        free(sl);
        return NULL;
    }

    A_INFO("created new symlist");

    return sl;
}

void _sym_list_free(SymbolList* sl) {
    if (sl != NULL) {
        free(sl->symbols);
    }
    free(sl);
}

void sym_list_add(SymbolList* sl, Symbol sym) {
    if (sl == NULL) { A_WARNING("cannot add symbol to NULL symbol list"); return; }
    if (sl->symbols == NULL) { A_WARNING("cannot add symbol to NULL symbol list ptr"); return; }

    // TODO: what if we run out of room lol
    sl->symbols[sl->length++] = sym;

}

void sym_list_print(const SymbolList sl) {
    for (size_t index = 0; index < sl.length; index++) {
        sym_print(sl.symbols[index]);
    }
}