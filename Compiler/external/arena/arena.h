#ifndef __ARENA_H
#define __ARENA_H

#include <stdlib.h>
#include "debug.h"

typedef struct arena {
    size_t size;
    size_t capacity;
    void* data;
    struct arena* next; // TODO: Make this actually functional & tested
} arena;

/// @brief Create a new arena instance with the given capacity.
/// @param capacity The maximum size of this arena in bytes.
/// @return The new arena instance.
arena* arena_new(size_t capacity);

/// @brief Deallocates the given arena.
/// @param arena The arena instance to deallocate.
#define arena_free(ptr) do { \
    _arena_free(ptr);        \
    ptr = NULL;              \
} while(0)                   \

/// @brief Private version of arena_free. Do not use this directly.
void _arena_free(arena* arena);

/// @brief Allocates the given number of bytes in the given arena.
/// @param arena The arena instance in which to allocate memory.
/// @param size The number of bytes to allocate.
/// @return A pointer to the allocated memory.
void* arena_alloc(arena* arena, size_t size);

#endif