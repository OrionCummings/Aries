#ifndef __BIG_INT_H
#define __BIG_INT_H

#include <stdint.h>
#include <stddef.h>

// An arbitrary bit signed 2's complement integer
// This implementation is not designed to be efficient; it's only goals are to be easy to use and to be correct.

typedef uint8_t byte;

typedef struct bint_t {
    byte* bytes;
    size_t n_bytes;
} bint_t;

bint_t* bint_new(size_t bytes);
void _bint_free(bint_t* b);


/// @brief 
/// @param result 
/// @param a 
/// @param b 
/// @return 
bint_t* bint_add(bint_t* result, const bint_t* const a, const bint_t* const b);

///
bint_t* bint_sub(bint_t* result, const bint_t* const a, const bint_t* const b);

///
bint_t* bint_mul(bint_t* result, const bint_t* const a, const bint_t* const b);

///
bint_t* bint_div(bint_t* result, const bint_t* const a, const bint_t* const b);

///
bint_t* bint_rem(bint_t* result, const bint_t* const a, const bint_t* const b);

///
bint_t* bint_mod(bint_t* result, const bint_t* const a, const bint_t* const b);

///
bint_t* bint_sqrt(bint_t* result, const bint_t* const a, const bint_t* const b);

///
bint_t* bint_pow(bint_t* result, const bint_t* const a, const bint_t* const b);

int bint_print(const bint_t a);

#endif