#include "util.h"


uint32_t extract_bits(uint32_t x, unsigned char start, unsigned char end) {
    if (end < start) { return 0; }
    return ((x >> start) & ((1u << (end - start)) - 1u));
}