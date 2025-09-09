#ifndef __ARENA_H
#define __ARENA_H

#include <stdlib.h>

typedef struct arena {
    size_t size;
    size_t capacity;
    void* data;
} arena;

arena arena_new(size_t capacity);
void arena_free(arena* arena);
void* arena_alloc(arena* arena, size_t size);

#endif