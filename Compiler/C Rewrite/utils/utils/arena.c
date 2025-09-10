#include "arena.h"

arena* arena_new(size_t capacity) {
    arena* a = calloc(1, sizeof(*a));

    if (a == NULL) {
        A_WARNING("failed to allocate arena");
        return NULL;
    }
    
    a->data = calloc(1, capacity);
    if (a->data == NULL) {
        A_WARNING("failed to allocate arena data");
        return NULL;
    }

    a->capacity = capacity;
    a->size = 0;
    
    return a;
}

void _arena_free(arena* a) {

    if (a != NULL) {
        free(a->data);
        a->data = NULL;
    }

    free(a);
}

void* arena_alloc(arena* a, size_t size) {
    
    if (a->size + size > a->capacity) {
        return NULL;
    }

    void* ptr = a->data + a->size;
    a->size += size;
    return ptr;
}
