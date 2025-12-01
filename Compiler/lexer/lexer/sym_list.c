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

void sym_list_add(SymbolList* symlist, Symbol sym) {
    if (symlist == NULL) { A_WARNING("cannot add symbol to NULL symbol list"); return; }
    if (symlist->symbols == NULL) { A_WARNING("cannot add symbol to NULL symbol list ptr"); return; }

    if (symlist->length == symlist->capacity) {
        void* temp = realloc(symlist->symbols, symlist->capacity * 2 * sizeof(*(symlist->symbols)));
        if (temp == NULL) {
            sym_list_free(symlist);
            A_ERROR("failed to reallocate symlist");
            return;
        }
        symlist->symbols = temp;
        symlist->capacity *= 2;
    }

    // Create a new string so the symbol owns it
    str* copy = str_copy(sym.s, 0, str_len(sym.s));

    // Copy the symbol
    void* dest = &(symlist->symbols[symlist->length]);
    void* src = &sym;
    size_t nbytes = sizeof(sym);
    memcpy(dest, src, nbytes);
    symlist->symbols[symlist->length].s = copy;

    symlist->length++;
}

void sym_list_print(const SymbolList sl) {
    for (size_t index = 0; index < sl.length; index++) {
        sym_print(sl.symbols[index]);
    }
}