#ifndef __BLOOM_FILTER_H
#define __BLOOM_FILTER_H

#include "debug.h"
#include "hash.h"
#include "arena.h"

typedef struct bfilter {
    size_t k;
    hash_function_t func;
    uint64_t bits;
} bfilter;

/// @brief Creates a new 64-bit bloom filter with `k` hash functions.
/// @param a The arena in which to allocate the filter.
/// @param k The number of hash functions.
/// @param func The hash function to be used in this filter.
/// @return A new filter struct.
bfilter* bfilter_anew(arena* a, size_t k, hash_function_t func);

/// @brief Adds the given hash object into the filter.
/// @param f The filter in which to add `obj`.
/// @param obj The object to add to the filter.
/// @return Returns false if the addition failed.
bool bfilter_add(bfilter* const f, hash_object_t obj);

/// @brief Determines if the given hash object `obj` is in the filter `f`.
/// @param f The filter in which to add the filter.
/// @param obj The object to add to the filter.
/// @return Returns false if the addition failed.
bool bfilter_in(bfilter* const f, hash_object_t obj);

#endif