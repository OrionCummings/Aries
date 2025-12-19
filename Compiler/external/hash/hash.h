#ifndef __HASH_H
#define __HASH_H

#include <stdint.h>
#include <stddef.h>

static const uint64_t BIG_PRIME = 15485863ul;

typedef uint64_t hash_t;

typedef struct hash_object_t {
    uint8_t* bytes;
    size_t n_bytes;
} hash_object_t;

typedef hash_t(*hash_function_t)(const hash_object_t, const uint64_t seed);

/// @brief Performs a hash of the given hash object. This is not a cryptographically secure hash; do not use for sensitive applications.
/// @param obj The object to be hashed.
/// @param seed An offset that yields a functionally different hash function.
/// @return A hash of `obj`.
hash_t hash(const hash_object_t obj, const uint64_t seed);

#endif