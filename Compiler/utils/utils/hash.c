#include "hash.h"

hash_t hash(const hash_object_t obj, const uint64_t seed) {

    if (obj.bytes == NULL) { return 0; }

    hash_t h = 117ul;
    hash_t p = 5381ul;
    hash_t pp = 593441843ul;

    for (size_t index = 0; index < obj.n_bytes * 8; index++) {
        h = ((h + obj.bytes[index] + seed) * p) % pp;
    }

    return h & 0xFFFFFFFF;
}
