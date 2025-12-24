#ifndef __BIG_INT_H
#define __BIG_INT_H

#include <stdint.h>
#include <stddef.h>
#include "str.h"
#include "arena.h"
#include "debug.h"

// An arbitrary-bit signed integer
// This implementation is not designed to be efficient; it's only goals are to be easy to use and to be correct.

typedef enum bint_error_t {

    // Indicate that the current state is not known but it is nonetheless an error. Additional enum fields should be added to notify users of specific errors. This state is not intended to be permanent; don't use it and don't rely on it.
    BINTE_UNKNOWN = -1,

    // Indicates that there is no error.
    BINTE_NONE = 0,

    // Indicates that the operation has overflowed and therefore that the result should not be used.
    BINTE_OVERFLOW,

    // Indicates that the operation has underflowed and therefore that the result should not be used.
    BINTE_UNDERFLOW,

    // Indicates that the operation attempted to divide by zero.
    BINTE_DIV_BY_ZERO,

    // Indicates that the operation attempted to use zero as a modulus.
    BINTE_MOD_BY_ZERO,

    // Indicates that the operation has lost or would lose some information in an unexpected (and therefore undesirable) manner.
    BINTE_LOST_INFO,

    // Indicates that the operation failed to allocate memory
    BINTE_MEMORY_ALLOCATION_FAILURE,

    // Indicates that the operation failed to write the result into the given space (via the `result` parameter).
    BINTE_INSUFFICIENT_RESULT_SIZE,

    // Indicates that an operation was provided an invalid parameter and cannot continue. This may be a null parameter or a zero length where a non-zero length was expected.
    BINTE_INVALID_PARAM,

} bint_error_t;

typedef enum bint_comp_t {

    // Indiates that the state of a comparison is unknown and is therefore an error.
    BINTC_UNKNOWN = -1,

    // The result of a comparison was false.
    BINTC_FALSE = 0,

    // The result of a comparison was true.
    BINTC_TRUE = 1,

    // TODO: Add more variations.

} bint_comp_t;

/// @brief The base of the bint. Used for printing.
typedef enum bint_base_t {
    BINT_BINARY = 0,
    BINT_OCTAL = 1,
    BINT_DECIMAL = 2,
    BINT_HEX = 3,
    BINT_B64 = 4,
} bint_base_t;

typedef struct bint_state_t {

    // Is the number positive? Zero is positive.
    uint8_t positive : 1;

    // Has the number (over|under)flowed? If so, this number can NOT be used in computation and any attempts to do so will generate/propagate errors. If you find yourself often encountering 'flows' then you should increase the size of your bints.
    uint8_t flowed : 1;

    // Is this number allocated in an arena? If so, we cannot free it ourselves!
    uint8_t managed : 1;
} bint_state_t;

/// @brief A big-integer struct.
///
/// Note that the contained bytes are stored such that the least significant byte is at index 0.
/// For example, the number 672345 = 0x0A4259 should be stored such that bytes = [0x59, 0x42, 0x0A]
typedef struct bint_t {
    bint_state_t state;
    size_t n_bytes;
    uint8_t* bytes;
} bint_t;

//////////////////// Object Management Operations ////////////////////

/// @brief Creates a new bint of the specified size.
/// @param bytes The size of the new bint in bytes.
/// @return A new bint.
bint_t* bint_new(size_t bytes);

/// @brief Creates a new bint of the specified size.
/// @param arena The arena in which to allocate this bint.
/// @param bytes The size of the new bint in bytes.
/// @return A new bint.
bint_t* bint_anew(arena* const arena, size_t bytes);

/// @brief Creates a new bint from the given string.
/// @param s A string containing the digits of the desired bint.
/// @return A new bint.
bint_t* bint_new_str(const str* const s);

/// @brief Creates a new bint from the given cstring.
/// @param s A cstring containing the digits of the desired bint.
/// @return A new bint.
bint_t* bint_new_cstr(const char* const s);

/// @brief Private function; do not use directly. Use `bint_free(...)`.
/// @return True if the b pointer was freed and false if it was not.
bool _bint_free(bint_t* b);

/// @brief Frees the given bint and sets it to zero.
/// @param b The bint instance to free.
#define bint_free(b) do{             \
    if (_bint_free(b)) { b = NULL; } \
} while(0)                           \

/// @brief Converts `a` into a str instance.
/// @param a An aribtrary-bit integer.
/// @param base The base in which to print the value of `a`.
/// @return The string instance containing `a`.
str* bint_to_str(const bint_t a, bint_base_t base);

/// @brief Converts `a` into a str instance.
/// @param arena The arena in which to allocate the str.
/// @param a An aribtrary-bit integer.
/// @param base The base in which to print the value of `a`.
/// @return The string instance containing `a`.
str* bint_to_astr(arena* const arena, const bint_t a, bint_base_t base);

/// @brief Prints the bint `a`.
/// @param a An aribtrary-bit integer.
/// @param base The base in which to print the value of `a`.
void bint_print(const bint_t a, bint_base_t base);

/// @brief Directly sets the bytes of `b`. This function is not meant to be used outside of test setups.
/// @param b The bint to modify.
/// @param bytes The bytes to write into `b`.
/// @param n_bytes The number of bytes to write into `b`.
/// @param offset The offset at which to write the bytes into `b`.
void bint_set_bytes(bint_t* const b, uint8_t* bytes, size_t n_bytes, size_t offset);

/// @brief Determines if the given bint_t is valid.
/// @param b An aribtrary-bit integer.
/// @return True if `b` is valid and false if `b` is not valid.
bool bint_valid(const bint_t* const b);

/// @brief Logs the given error.
/// @param err The error to be logged.
void bint_log_error(bint_error_t err);

//////////////////// Bitwise Operations ////////////////////

/// @brief Calculates the bitwise NOT of the value of `a`.
/// @param result The location in which to place the result of `~a`.
/// @param a An aribtrary-bit integer.
/// @return Zero on success; otherwise, an error code.
bint_error_t bint_not(bint_t** result, const bint_t* const a);

/// @brief Calculates the bitwise AND of the value of `a`.
/// @param result The location in which to place the result of `a & b`.
/// @param a An aribtrary-bit integer.
/// @param b An aribtrary-bit integer.
/// @return Zero on success; otherwise, an error code.
bint_error_t bint_and(bint_t** result, const bint_t* const a, const bint_t* const b);

/// @brief Calculates the bitwise OR of the value of `a`.
/// @param result The location in which to place the result of `a | b`.
/// @param a An aribtrary-bit integer.
/// @param b An aribtrary-bit integer.
/// @return Zero on success; otherwise, an error code.
bint_error_t bint_or(bint_t** result, const bint_t* const a, const bint_t* const b);

/// @brief Calculates the bitwise NOR of the value of `a`.
/// @param result The location in which to place the result of `~(a | b)`.
/// @param a An aribtrary-bit integer.
/// @param b An aribtrary-bit integer.
/// @return Zero on success; otherwise, an error code.
bint_error_t bint_nor(bint_t** result, const bint_t* const a, const bint_t* const b);

/// @brief Calculates the bitwise NAND of the value of `a`.
/// @param result The location in which to place the result of `~(a & b)`.
/// @param a An aribtrary-bit integer.
/// @param b An aribtrary-bit integer.
/// @return Zero on success; otherwise, an error code.
bint_error_t bint_nand(bint_t** result, const bint_t* const a, const bint_t* const b);

/// @brief Calculates the bitwise XOR of the value of `a`.
/// @param result The location in which to place the result of `a ^ b`.
/// @param a An aribtrary-bit integer.
/// @param b An aribtrary-bit integer.
/// @return Zero on success; otherwise, an error code.
bint_error_t bint_xor(bint_t** result, const bint_t* const a, const bint_t* const b);

/// @brief Calculates the bitwise XNOR of the value of `a`.
/// @param result The location in which to place the result of `~(a ^ b)`.
/// @param a An aribtrary-bit integer.
/// @param b An aribtrary-bit integer.
/// @return Zero on success; otherwise, an error code.
bint_error_t bint_xnor(bint_t** result, const bint_t* const a, const bint_t* const b);

/// @brief Calculates the bitwise left shift of the value of `a` by `bits` bits.
/// @param result The location in which to place the result of `a << bits`.
/// @param a An aribtrary-bit integer.
/// @param bits The number of bits to shift.
/// @return Zero on success; otherwise, an error code.
bint_error_t bint_shl(bint_t** result, const bint_t* const a, const uint64_t bits);

/// @brief Calculates the bitwise right shift of the value of `a` by `bits` bits.
/// @param result The location in which to place the result of `a >> bits`.
/// @param a An aribtrary-bit integer.
/// @param bits The number of bits to shift.
/// @return Zero on success; otherwise, an error code.
bint_error_t bint_shr(bint_t** result, const bint_t* const a, const uint64_t bits);

/// @brief Calculates the bitwise left rotation of the value of `a` by `bits` bits.
/// @param result The location in which to place the result of `a <<< bits`.
/// @param a An aribtrary-bit integer.
/// @param bits The number of bits to shift.
/// @return Zero on success; otherwise, an error code.
bint_error_t bint_rotr(bint_t** result, const bint_t* const a, const uint64_t bits);

/// @brief Calculates the bitwise right rotation of the value of `a` by `bits` bits.
/// @param result The location in which to place the result of `a >>> bits`.
/// @param a An aribtrary-bit integer.
/// @param bits The number of bits to shift.
/// @return Zero on success; otherwise, an error code.
bint_error_t bint_rotl(bint_t** result, const bint_t* const a, const uint64_t bits);

//////////////////// Comparison Operations ////////////////////

/// @brief Determines if two bints are equal.
/// @param comp The result of a comparison.
/// @param a An aribtrary-bit integer.
/// @param b An aribtrary-bit integer.
/// @return Zero on success; otherwise, an error code.
bint_error_t bint_eq(bint_comp_t* const comp, const bint_t* const a, const bint_t* const b);

/// @brief Determines if two bints are not equal.
/// @param comp The result of a comparison.
/// @param a An aribtrary-bit integer.
/// @param a An aribtrary-bit integer.
/// @return Zero on success; otherwise, an error code.
bint_error_t bint_neq(bint_comp_t* const comp, const bint_t* const a, const bint_t* const b);

/// @brief Given two bints `a` and `b`, determines if `a < b`.
/// @param comp The result of a comparison.
/// @param a An aribtrary-bit integer.
/// @param a An aribtrary-bit integer.
/// @return Zero on success; otherwise, an error code.
bint_error_t bint_lt(bint_comp_t* const comp, const bint_t* const a, const bint_t* const b);

/// @brief Given two bints `a` and `b`, determines if `a <= b`.
/// @param comp The result of a comparison.
/// @param a An aribtrary-bit integer.
/// @param a An aribtrary-bit integer.
/// @return Zero on success; otherwise, an error code.
bint_error_t bint_lte(bint_comp_t* const comp, const bint_t* const a, const bint_t* const b);

/// @brief Given two bints `a` and `b`, determines if `a > b`.
/// @param comp The result of a comparison.
/// @param a An aribtrary-bit integer.
/// @param a An aribtrary-bit integer.
/// @return Zero on success; otherwise, an error code.
bint_error_t bint_gt(bint_comp_t* const comp, const bint_t* const a, const bint_t* const b);

/// @brief Given two bints `a` and `b`, determines if `a >= b`.
/// @param comp The result of a comparison.
/// @param a An aribtrary-bit integer.
/// @param a An aribtrary-bit integer.
/// @return Zero on success; otherwise, an error code.
bint_error_t bint_gte(bint_comp_t* const comp, const bint_t* const a, const bint_t* const b);

//////////////////// Simple Operations ////////////////////

/// @brief Adds the value of `a` to the value of `b`.
/// @param result The location in which to place the result of `a + b`.
/// @param a An aribtrary-bit integer.
/// @param b An aribtrary-bit integer.
/// @return Zero on success; otherwise, an error code.
bint_error_t bint_add(bint_t** result, const bint_t* const a, const bint_t* const b);

/// @brief Subtracts the value of `b` from the value of `a`.
/// @param result The location in which to place the result of `b - a`.
/// @param a An aribtrary-bit integer.
/// @param b An aribtrary-bit integer.
/// @return Zero on success; otherwise, an error code.
bint_error_t bint_sub(bint_t** result, const bint_t* const a, const bint_t* const b);

/// @brief Multiplies the value of `a` with the value of `b`.
/// @param result The location in which to place the result of `a * b`.
/// @param a An aribtrary-bit integer.
/// @param b An aribtrary-bit integer.
/// @return Zero on success; otherwise, an error code.
bint_error_t bint_mul(bint_t** result, const bint_t* const a, const bint_t* const b);

/// @brief Divides the value of `a` by the value of `b`.
/// @param result The location in which to place the result of `a / b`.
/// @param a An aribtrary-bit integer.
/// @param b An aribtrary-bit integer.
/// @return Zero on success; otherwise, an error code.
bint_error_t bint_div(bint_t** result, const bint_t* const a, const bint_t* const b);

/// @brief Calculates the modulo of the value of `a` by the value of `b`.
/// @param result The location in which to place the result of `a % b`.
/// @param a An aribtrary-bit integer.
/// @param b An aribtrary-bit integer.
/// @return Zero on success; otherwise, an error code.
bint_error_t bint_mod(bint_t** result, const bint_t* const a, const bint_t* const b);

//////////////////// Complex Operations ////////////////////

/// @brief Calculates the square root of `a`.
/// @param result The location in which to place the result of `sqrt(a)`.
/// @param a An aribtrary-bit integer.
/// @return Zero on success; otherwise, an error code.
bint_error_t bint_sqrt(bint_t** result, const bint_t* const a);

/// @brief Calculates `a` to the `b`-th power.
/// @param result The location in which to place the result of `a^b`.
/// @param a An aribtrary-bit integer.
/// @param b An aribtrary-bit integer.
/// @return Zero on success; otherwise, an error code.
bint_error_t bint_pow(bint_t** result, const bint_t* const a, const bint_t* const b);

#endif