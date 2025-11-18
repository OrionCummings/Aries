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

    return sl;
}

void _sym_list_free(SymbolList* sl) {
    if (sl != NULL) {
        free(sl->symbols);
    }
    free(sl);
}

void sym_list_add(SymbolList* sl, const Symbol* sym) {
    if (sl == NULL) { A_WARNING("cannot add symbol to NULL symbol list"); return; }
    if (sym == NULL) { A_WARNING("cannot add NULL symbol to symbol list"); return; }
    if (sl->symbols == NULL) { A_WARNING("cannot add symbol to NULL symbol list ptr"); return; }

    if (sl->length == sl->capacity) {
        void* temp = realloc(sl->symbols, (sl->capacity * 2) * sizeof(*(sl->symbols)));

        if (temp == NULL) { A_WARNING("failed to reallocate symbol list"); return; }

        sl->symbols = temp;
        sl->capacity *= 2;
    }

    // TODO: Add null checks
    str* temp_str = str_copy(sym->s, 0, str_len(sym->s));

    size_t offset = (sl->length);
    void* next = sl->symbols + offset;
    memcpy(next, sym, sizeof(*sym));
    // memcpy();

    sym_free(sym);

    sl->length++;
}

void sym_list_print(const SymbolList sl) {
    for (size_t index = 0; index < sl.length; index++) {
        sym_print(sl.symbols[index]);
    }
}