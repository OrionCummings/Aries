#include "bint.h"

//////////////////// Object Management Operations ////////////////////

bint_t* bint_new(size_t bytes) {

    if (bytes == 0) {
        return NULL;
    }

    bint_t* b = calloc(1, sizeof(*b));
    if (b == NULL) {
        return NULL;
    }

    b->bytes = calloc(bytes, sizeof(*b->bytes));
    if (b->bytes == NULL) {
        return NULL;
    }

    b->n_bytes = bytes;
    b->state = (bint_state_t){ .flowed = false, .positive = true, .managed = false };

    A_INFO("created a new %d-byte bint", bytes);

    return b;
}

bint_t* bint_anew(arena* const arena, size_t bytes) {

    if (bytes == 0) {
        return NULL;
    }

    bint_t* b = arena_alloc(arena, sizeof(*b));
    if (b == NULL) {
        return NULL;
    }

    b->bytes = arena_alloc(arena, bytes * sizeof(*b->bytes));
    if (b->bytes == NULL) {
        return NULL;
    }

    b->n_bytes = bytes;
    b->state = (bint_state_t){ .flowed = false, .positive = true, .managed = true };

    A_INFO("created a new %d-byte bint in arena 0x%p", bytes, arena);

    return b;
}

// TODO: NOT COMPLETE!
bint_t* bint_new_str(const str* const s) {

    return NULL;

    if (s == NULL) {
        return NULL;
    }
    if (s->data == NULL) {
        return NULL;
    }

    arena* scratchpad = arena_new(2048, 4); // TODO: Magic number!
    size_t len = str_len(s);

    // TODO: Use the string length to calculate an upper bound on allocated bytes.
    bint_t* b = bint_new(1024); // TODO: Magic number!

    bint_t* scale;
    bint_t* digit;
    bint_t* placed_digit;
    for (index_t digit_index = 0; digit_index < len; digit_index++) {

        // Get the character and make sure it's a valid digit
        char c = s->data[len - digit_index - 1];
        if (c < '0' || '9' < c) {
            A_ERROR("invalid digit '%c' at index %i", c, digit_index);
            return NULL;
        }

        uint8_t numeric_digit = (uint8_t)(c - '0');

        scale = bint_new(64); // TODO: Magic number!
        digit = bint_new(64); // TODO: Magic number!

        bint_error_t err = bint_mul(&placed_digit, digit, scale);
        if (err) {
            bint_log_error(err);
            A_ERROR("failed to place digit");

            bint_free(digit);
            bint_free(placed_digit);

            return NULL;
        }

        bint_free(digit);
        bint_free(placed_digit);
    }

    // Free the scratchpad arena
    arena_free(scratchpad);

    A_INFO("created a new XXX-byte bint from a string"); // TODO: Update with final size calculation.

    return NULL;
}

bint_t* bint_new_cstr(const char* const s) {

    str* str = str_new(s);
    if (str == NULL || str->data == NULL) {
        return NULL;
    }

    bint_t* b = bint_new_str(str);
    if (b == NULL || b->bytes == NULL) {
        return NULL;
    }

    str_free(str);

    return b;
}

bool _bint_free(bint_t* b) {

    if (b == NULL) {
        return false;
    }
    if (b->bytes == NULL) {
        return false;
    }
    if (b->n_bytes == 0) {
        return false;
    }
    if (b->state.managed) {
        return false;
    }

    free(b->bytes);
    free(b);

    A_INFO("freed bint"); // TODO: Update with final size calculation.

    return true;
}

str* bint_to_str(const bint_t a, bint_base_t base) { return NULL; }

str* bint_to_astr(arena* const arena, const bint_t a, bint_base_t base) { return NULL; }

void bint_print(const bint_t a, bint_base_t base) {

    str* s = bint_to_str(a, base);
    if (s == NULL || s->data == NULL) {
        return;
    }

    str_print("", s);

    str_free(s);
    return;
}

void bint_set_bytes(bint_t* const b, uint8_t* bytes, size_t n_bytes, size_t offset) {
    if (b == NULL || b->bytes == NULL) {
        return;
    }
    if (bytes == NULL) {
        return;
    }
    if (n_bytes + offset > b->n_bytes) {
        return;
    }
    if (n_bytes == 0) {
        return;
    }

    memcpy(&b->bytes[offset], bytes, n_bytes);
}

bool bint_valid(const bint_t* const b) { return !(b == NULL || b->bytes == NULL || b->n_bytes == 0); }

void bint_log_error(bint_error_t err) {

    switch (err) {
    case (BINTE_NONE): {
        A_INFO("no bint error");
        break;
    }

    case (BINTE_UNKNOWN): {
        A_ERROR("unknown bint error");
        break;
    }

    case (BINTE_OVERFLOW): {
        A_ERROR("bint overflow");
        break;
    }

    case (BINTE_UNDERFLOW): {
        A_ERROR("bint underflow");
        break;
    }

    case (BINTE_DIV_BY_ZERO): {
        A_ERROR("bint divided by zero");
        break;
    }

    case (BINTE_MOD_BY_ZERO): {
        A_ERROR("bint mod by zero");
        break;
    }

    case (BINTE_LOST_INFO): {
        A_ERROR("bint operation has lost or may lose information");
        break;
    }

    case (BINTE_MEMORY_ALLOCATION_FAILURE): {
        A_ERROR("bint memory allocation failure");
        break;
    }

    case (BINTE_INSUFFICIENT_RESULT_SIZE): {
        A_ERROR("insufficient bint result size");
        break;
    }

    case (BINTE_INVALID_PARAM): {
        A_ERROR("invalid parameter encountered");
        break;
    }
    }
}

//////////////////// Bitwise Operations ////////////////////

bint_error_t bint_not(bint_t** result, const bint_t* const a) {
    if (!bint_valid(a) || result == NULL) {
        return BINTE_INVALID_PARAM;
    }
    if (*result != NULL) {
        return BINTE_LOST_INFO;
    }

    *result = bint_new(a->n_bytes);
    if (result == NULL || *result == NULL || (*result)->bytes == NULL) {
        return BINTE_MEMORY_ALLOCATION_FAILURE;
    }

    for (index_t index = 0; index < a->n_bytes; index++) {
        (*result)->bytes[index] = ~(a->bytes[index]);
    }

    return BINTE_NONE;
}

bint_error_t bint_and(bint_t** result, const bint_t* const a, const bint_t* const b) {
    if (!bint_valid(a) || !bint_valid(b) || result == NULL) {
        return BINTE_INVALID_PARAM;
    }
    if (*result != NULL) {
        return BINTE_LOST_INFO;
    }

    size_t max_size, min_size, temp_size;

    // Guess the order
    max_size = a->n_bytes;
    min_size = b->n_bytes;

    // If we were wrong, then swap them
    if (max_size < min_size) {
        temp_size = max_size;
        max_size = min_size;
        min_size = temp_size;
    }

    assert(max_size >= min_size);

    *result = bint_new(max_size);
    if (result == NULL || *result == NULL || (*result)->bytes == NULL) {
        return BINTE_MEMORY_ALLOCATION_FAILURE;
    }

    for (index_t index = 0; index < min_size; index++) {
        (*result)->bytes[index] = (a->bytes[index] & b->bytes[index]);
    }

    // NOTE:
    // We are assuming bytes beyond 'min_size' of the small bint to be zero
    // => any result of AND(x, 0) = 0 which is the default value
    // => we don't have to do anything. This will NOT necessarily be the case for other operations!!

    return BINTE_NONE;
}

bint_error_t bint_nand(bint_t** result, const bint_t* const a, const bint_t* const b) {
    if (!bint_valid(a) || !bint_valid(b) || result == NULL) {
        return BINTE_INVALID_PARAM;
    }
    if (*result != NULL) {
        return BINTE_LOST_INFO;
    }

    bint_t* r1 = NULL;
    bint_error_t err;

    err = bint_and(&r1, a, b);
    if (err) {
        return err;
    }

    err = bint_not(result, r1);
    if (err) {
        return err;
    }

    bint_free(r1);

    return BINTE_NONE;
}

bint_error_t bint_or(bint_t** result, const bint_t* const a, const bint_t* const b) {
    if (!bint_valid(a) || !bint_valid(b) || result == NULL) {
        return BINTE_INVALID_PARAM;
    }
    if (*result != NULL) {
        return BINTE_LOST_INFO;
    }

    size_t max_size, min_size, temp_size;

    // Guess the order
    bool a_is_larger = true;
    max_size = a->n_bytes;
    min_size = b->n_bytes;

    // If we were wrong, then swap them
    if (max_size < min_size) {
        temp_size = max_size;
        max_size = min_size;
        min_size = temp_size;
        a_is_larger = false;
    }

    assert(max_size >= min_size);

    *result = bint_new(max_size);
    if (result == NULL || *result == NULL || (*result)->bytes == NULL) {
        return BINTE_MEMORY_ALLOCATION_FAILURE;
    }

    for (index_t index = 0; index < min_size; index++) {
        (*result)->bytes[index] = (a->bytes[index] | b->bytes[index]);
    }

    const bint_t* const temp = (a_is_larger) ? a : b;
    for (index_t index = min_size; index < max_size; index++) {
        (*result)->bytes[index] = (temp->bytes[index]);
    }

    return BINTE_NONE;
}

bint_error_t bint_nor(bint_t** result, const bint_t* const a, const bint_t* const b) {
    if (!bint_valid(a) || !bint_valid(b) || result == NULL) {
        return BINTE_INVALID_PARAM;
    }
    if (*result != NULL) {
        return BINTE_LOST_INFO;
    }

    bint_t* r1 = NULL;
    bint_error_t err;

    err = bint_or(&r1, a, b);
    if (err) {
        return err;
    }

    err = bint_not(result, r1);
    if (err) {
        return err;
    }

    bint_free(r1);

    return BINTE_NONE;
}

bint_error_t bint_xor(bint_t** result, const bint_t* const a, const bint_t* const b) { return BINTE_UNKNOWN; }

bint_error_t bint_xnor(bint_t** result, const bint_t* const a, const bint_t* const b) { return BINTE_UNKNOWN; }

bint_error_t bint_shl(bint_t** result, const bint_t* const a, const uint64_t bits) { return BINTE_UNKNOWN; }

bint_error_t bint_shr(bint_t** result, const bint_t* const a, const uint64_t bits) { return BINTE_UNKNOWN; }

bint_error_t bint_rotr(bint_t** result, const bint_t* const a, const uint64_t bits) { return BINTE_UNKNOWN; }

bint_error_t bint_rotl(bint_t** result, const bint_t* const a, const uint64_t bits) { return BINTE_UNKNOWN; }

//////////////////// Simple Operations ////////////////////

bint_error_t bint_add(bint_t** result, const bint_t* const a, const bint_t* const b) { return BINTE_UNKNOWN; }

bint_error_t bint_sub(bint_t** result, const bint_t* const a, const bint_t* const b) { return BINTE_UNKNOWN; }

bint_error_t bint_mul(bint_t** result, const bint_t* const a, const bint_t* const b) { return BINTE_UNKNOWN; }

bint_error_t bint_div(bint_t** result, const bint_t* const a, const bint_t* const b) { return BINTE_UNKNOWN; }

bint_error_t bint_mod(bint_t** result, const bint_t* const a, const bint_t* const b) { return BINTE_UNKNOWN; }

//////////////////// Complex Operations ////////////////////

bint_error_t bint_sqrt(bint_t** result, const bint_t* const a) { return BINTE_UNKNOWN; }

bint_error_t bint_pow(bint_t** result, const bint_t* const a, const bint_t* const b) { return BINTE_UNKNOWN; }
