#include "arena.h"

arena arena_new(size_t capacity) {
    arena a = {0};

    a.data = calloc(1, capacity);
    a.capacity = capacity;
    a.size = 0;
    
    return a;
}

void arena_free(arena* arena) {
    free(arena->data);
    arena->data = NULL;

}

void* arena_alloc(arena* arena, size_t size) {
    
    if (arena->size + size > arena->capacity) {
        return NULL;
    }

    void* ptr = (void*)(arena + arena->size);
    arena->size += size;
    return ptr;
}
