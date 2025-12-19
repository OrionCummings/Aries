#include "bloom_filter.h"

bfilter* bfilter_anew(arena* a, size_t k, hash_function_t func) {

    if (a == NULL || k == 0) { return NULL; }

    bfilter* f = arena_alloc(a, sizeof(*f));
    if (f == NULL) { return NULL; }

    f->func = func;
    f->k = k;

    A_INFO("created new bloom filter with 64 bits and %lu hash functions", k);

    return f;
}

bool bfilter_add(bfilter* const f, hash_object_t obj) {
    if (f == NULL || f->k == 0 || obj.n_bytes == 0 || obj.bytes == NULL) { return NULL; }

    uint64_t hashes[f->k];
    for (size_t index = 0; index < f->k; index++) {
        f->bits |= f->func(obj, index);
    }

    A_INFO("added a %li-byte object to a bfilter", obj.n_bytes);

    return true; // TODO: Make this return something meaningful.
}

bool bfilter_in(bfilter* const f, hash_object_t obj) {
    if (f == NULL || f->k == 0 || obj.n_bytes == 0 || obj.bytes == NULL) { return NULL; }

    uint64_t bits;
    uint64_t hashes[f->k];
    for (size_t index = 0; index < f->k; index++) {
        bits |= f->func(obj, index);
    }

    for (size_t index = 0; index < 64; index++) {
        if ((bits & (1 << index)) ^ (f->bits & (1 << index))) {
            A_INFO("failed to find item in bfilter");
            return false;
        }
    }

    A_INFO("found item in bfilter");
    return true;
}
