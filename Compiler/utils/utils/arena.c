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
    a->next = NULL;

    return a;
}

void _arena_free(arena* a) {

    if (a != NULL) {
        free(a->data);
        a->data = NULL;

        if (a->next != NULL) {
            _arena_free(a->next);
            a->next = NULL;
        }
    }

    free(a);
}

void* arena_alloc(arena* a, size_t size) {

    if (a == NULL) {
        A_WARNING("Failed to allocate memory from a null arena");
        return NULL;
    }

    if (size == 0) {
        A_WARNING("Requested zero bytes from an arena");
        return NULL;
    }

    // If the requested size is larger than the capacity of the arena, then we can't store it even by creating new arenas so fail out!
    // We COULD decide to allow non-contiguous memory regions to be managed by the arena, but that is beyond the scope of the current implementation.
    if (size > a->capacity) {
        A_WARNING("Cannot create non-contiguous memory regions with the given size (%lu > %lu)", size, a->capacity);
        return NULL;
    }

    // If the requested amount of memory would not fit in the current arena, then create a new arena and forward the memory request there
    if (a->size + size > a->capacity) {

        // If there is no next arena, make one
        if (a->next == NULL) {
            a->next = arena_new(a->capacity);

            // If we fail to create a new next arena, then we fail
            if (a->next == NULL) {
                A_WARNING("Failed to create next arena");
                return NULL;
            }
        }

        // If there is a next arena, then forward the request
        void* next_ptr = arena_alloc(a->next, size);

        // If the next arena can't handle it, then we fail
        if (next_ptr == NULL) {
            A_WARNING("Failed to allocate more memory in an arena");
            return NULL;
        }

        // Return the address from the next arena
        return next_ptr;
    }

    // If there is space in this arena, then calculate the next available offset and return it
    void* ptr = a->data + a->size;
    a->size += size;
    return ptr;
}
