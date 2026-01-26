#include "arena.h"

arena* arena_new(size_t capacity) {
    arena* a = calloc(1, sizeof(*a));

    if (a == NULL) {
        A_ERROR("failed to allocate arena");
        return NULL;
    }

    a->data = calloc(1, capacity);
    if (a->data == NULL) {
        A_ERROR("failed to allocate arena data");
        return NULL;
    }

    a->capacity = capacity;
    a->size = 0;
    a->next = NULL;

    A_INFO("created new arena");

    return a;
}

void _arena_free(arena* a) {

    if (a != NULL) {
        free(a->data);
        a->data = NULL;

        if (a->next != NULL) {
            A_INFO("freeing a child arena");
            _arena_free(a->next);
            a->next = NULL;
        }
    }

    free(a);
    A_INFO("freed an arena");
}

void* arena_alloc(arena* a, size_t size) {

    if (a == NULL) {
        A_ERROR("failed to allocate memory from a null arena");
        return NULL;
    }

    if (size == 0) {
        A_ERROR("requested zero bytes from an arena");
        return NULL;
    }

    // If the requested size is larger than the capacity of the arena, then we can't store it even by creating new arenas so fail out!
    // We COULD decide to allow non-contiguous memory regions to be managed by the arena, but that is beyond the scope of the current implementation.
    if (size > a->capacity) {
        A_ERROR("cannot create non-contiguous memory regions with the given size (%lu > %lu)", size, a->capacity);
        return NULL;
    }

    // If the requested amount of memory would not fit in the current arena, then create a new arena and forward the memory request there
    if (a->size + size > a->capacity) {

        // If there is no next arena, make one
        if (a->next == NULL) {
            a->next = arena_new(a->capacity);

            // If we fail to create a new next arena, then we fail
            if (a->next == NULL) {
                A_ERROR("failed to create next arena");
                return NULL;
            }
        }

        // If there is a next arena, then forward the request
        void* next_ptr = arena_alloc(a->next, size);

        // If the next arena can't handle it, then we fail
        if (next_ptr == NULL) {
            A_ERROR("failed to allocate more memory in an arena");
            return NULL;
        }

        A_INFO("allocated %lu %s from a child arena", size, ((size > 1)? "bytes" : "byte"));
        
        // Return the address from the next arena
        return next_ptr;
    }
    
    // If there is space in this arena, then calculate the next available offset and return it
    void* ptr = a->data + a->size;
    a->size += size;
    
    A_INFO("allocated %lu %s from an arena", size, ((size > 1)? "bytes" : "byte"));

    return ptr;
}

void arena_reset(arena* const arena) {
    if (arena == NULL) {
        A_ERROR("passed null arena");
        return;
    }

    if (arena->next != NULL) {
        arena_reset(arena->next);
    }

    memset(arena->data, 0, arena->capacity); // TODO: Figure out of this is a bad idea? Is this slow? Do I care?
    arena->size = 0; // TODO: This behavior breaks a previous invariant: unused memory was previously zero! Is this ok? What value does this invariant bring? Are we relying on it?
    A_INFO("reset arena");
}
