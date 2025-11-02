#include "sym_list.h"

SymbolList* sym_list_new(const size_t capacity) {
    SymbolList* sl = calloc(1, sizeof(*sl));

    if (sl == NULL) {
        A_WARNING("Failed to allocate new sym list object");
        return NULL;
    }

    sl->capacity = capacity;
    sl->length = 0;
    sl->symbols = calloc(capacity, sizeof(*sl->symbols));

    if (sl->symbols == NULL) {
        A_WARNING("Failed to allocate new symbol list in a sym list object");
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

void sym_list_add(SymbolList* sl, Symbol* sym) {
    if (sl == NULL) {
        A_WARNING("Cannot add symbol to NULL symbol list");
        return;
    }

    if (sl->length == sl->capacity) {
        void* temp = realloc(sl->symbols, sl->capacity * 2);

        if (temp == NULL) {
            A_WARNING("Failed to reallocate symbol list");
            return;
        }

        sl->symbols = temp;
        sl->capacity *= 2;
    }

    memcpy((sl->symbols + (sl->length * sizeof(*sym))), sym, sizeof(*sym));

    sl->length++;
}