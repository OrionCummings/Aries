#include "str.h"

str* str_new(const char* s) {

    if (s == NULL) {
        return NULL;
    }

    str* r = calloc(1, sizeof(*r));

    if (r == NULL) {
        return NULL;
    }

    size_t len = strlen(s);

    r->data = calloc(len, sizeof(*(r->data)));

    strncpy(r->data, s, len);

    r->length = len;
    r->location = AL_HEAP;

    return r;
}

str* astr_new(arena* const a, const char* cstr) {
    if (cstr == NULL || a == NULL) {
        return NULL;
    }

    str* s = arena_alloc(a, sizeof(*s));

    if (s == NULL) {
        return NULL;
    }

    size_t len = strlen(cstr);
    s->data = arena_alloc(a, len * sizeof(*(s->data)));
    strncpy(s->data, cstr, len);

    s->length = len;
    s->location = AL_ARENA;

    return s;
}

void _str_free(str* s) {

    // Only free heap-allocated strings! Don't attempt to free a stack-allocated
    // or arena-allocated string!
    if (s != NULL && (s->location == AL_HEAP)) {
        free(s->data);
    }

    free(s);
}

str* str_concat(str* s1, str* s2) {

    if (s1 == NULL || s2 == NULL) {
        return NULL;
    }

    if (s1->data == NULL || s2->data == NULL) {
        return NULL;
    }

    // Get the length of both input strings
    size_t len_s1 = str_len(s1);
    size_t len_s2 = str_len(s2);
    size_t new_len = len_s1 + len_s2 + 1; // +1 for null byte

    // Create a space that can fit both of them
    char dest[new_len];
    memset((void*)dest, 0, new_len);

    strcpy(dest, s1->data);
    strcat(dest, s2->data);

    str* concat = str_new(dest);

    return concat;
}

bool str_cmp(const str* const s1, const str* const s2) {

    if ((s1 == NULL) ^ (s2 == NULL)) {
        return false;
    }

    size_t len_s1 = str_len(s1);
    if (len_s1 != str_len(s2)) {
        return false;
    }

    for (index_t i = 0; i < len_s1; i++) {
        char a = s1->data[i];
        char b = s2->data[i];
        if (a != b) {
            return false;
        }
    }
    return true;
}

bool str_cmp_raw(const str* const s, const char* const cs) {

    if (s == NULL || s->data == NULL || cs == NULL) {
        return false;
    }
    size_t len_s = str_len(s);
    size_t len_cs = strlen(cs);
    if (len_s != len_cs) {
        return false;
    }
    return strncmp(s->data, cs, len_s) == 0;
}

bool str_ident(const str* const s1, const str* const s2) {
    return (s1 != NULL) && (s2 != NULL) && (s1->location == s2->location) && (s1->length == s2->length)
        && (str_cmp(s1, s2));
}

int str_find(const str* const s, const char c) {

    if (s == NULL) {
        return -1;
    }

    for (size_t index = 0; index < str_len(s); index++) {
        if (str_at(s, index) == c) {
            return index;
        }
    }

    return -1;
}

int str_sub(const str* const s, const str* const sub) {

    if (s == NULL || sub == NULL) {
        return -1;
    }

    size_t len_s = str_len(s);
    size_t len_sub = str_len(sub);

    // If the length of the sub string is greater than the string, then there is
    // no way for it to be a sub string
    if (len_sub > len_s) {
        return -1;
    }

    bool possible_sub = false;
    int possible_sub_index = -1;
    for (size_t index = 0; index < len_s; index++) {
        for (size_t sub_index = 0; sub_index < len_sub; sub_index++) {
            if (str_at(s, index) != str_at(sub, sub_index)) {
                break;
            }

            if (sub_index == len_sub) {
                return index - len_sub;
            }
        }
    }

    return -1;
}

size_t str_len(const str* s) {
    if (s == NULL || s->data == NULL) {
        return 0;
    }

    return s->length;
}

char str_at(const str const* s, size_t index) {
    if (s == NULL) {
        return 0;
    }

    size_t length = str_len(s);

    if (index > length) {
        return 0;
    }

    return s->data[index];
}

str* str_append(const str* const s, const char c) {
    if (s == NULL || (s->location != AL_HEAP) || c == '\0') {
        return NULL;
    }

    size_t length = str_len(s);
    char buffer[length + 1];       // null byte
    memset(buffer, 0, length + 1); // null byte

    (void)snprintf(buffer, length + 2, "%s%c", s->data,
                   c); // new char + null byte

    return str_new((char*)buffer); // get that nasty array away!!! Yuck!
}

str str_view(const str* const s, size_t start, size_t end) {
    if (s == NULL || start >= end) {
        return STR_EMPTY;
    }

    size_t len = str_len(s);
    if (len == 0 || start > len || end > len) {
        return STR_EMPTY;
    }

    str view = { .data = s->data + start, .length = end - start, .location = AL_STACK };
    return view;
}

str* str_copy(const str const* s, size_t start, size_t end) {
    if (s == NULL || start >= end) {
        return NULL;
    }

    size_t len = str_len(s);
    if (len == 0 || start > len || end > len) {
        return NULL;
    }

    size_t len_substring = end - start;

    char substring[len_substring + 1];
    memset(substring, 0, len_substring + 1);
    memcpy(substring, s->data + start, len_substring);

    return str_new((char*)substring);
}

str* astr_copy(arena* const a, str* s, size_t start, size_t end) {
    if (s == NULL || a == NULL || start >= end) {
        return NULL;
    } // TODO: Are these conditions correct?

    size_t len = str_len(s);
    if (len == 0 || start > len || end > len) {
        return NULL;
    }

    size_t len_substring = end - start;

    char substring[len_substring + 1];
    memset(substring, 0, len_substring + 1);
    memcpy(substring, s->data + start, len_substring);

    return astr_new(a, (char*)substring);
}

char* str_raw(const str* const s) {
    if (s == NULL || s->data == NULL) {
        return NULL;
    }

    size_t len_s = str_len(s);
    void* ptr = calloc(len_s + 1, sizeof(char));
    if (ptr == NULL) {
        return NULL;
    }

    strncpy(ptr, s->data, len_s);
    return (char*)ptr;
}

str* str_from_file(FILE* const file) {

    if (file == NULL) {
        return NULL;
    }

    fseek(file, 0, SEEK_END);
    size_t len = ftell(file);
    fseek(file, 0, SEEK_SET);

    char* buffer = calloc(len + 1, sizeof(*buffer));
    if (buffer == NULL) {
        return NULL;
    }
    fread(buffer, 1, len, file);
    buffer[len] = '\0';

    str* s = str_new(buffer);
    free(buffer);

    return s;
}

str* astr_from_file(arena* const a, FILE* const file) {
    if (file == NULL) {
        return NULL;
    }

    fseek(file, 0, SEEK_END);
    size_t len = ftell(file);
    fseek(file, 0, SEEK_SET);

    char* buffer = arena_alloc(a, sizeof(*buffer) * len);
    if (buffer == NULL) {
        return NULL;
    }
    fread(buffer, 1, len, file);

    str* s = astr_new(a, buffer);
    return s;
}

str* str_from_filename(const char* filename) {
    if (filename == NULL) {
        return NULL;
    }

    FILE* file = fopen(filename, "r");
    if (file == NULL) {
        return NULL;
    }

    str* s = str_from_file(file);
    if (file == NULL) {
        return NULL;
    }

    fclose(file);

    return s;
}

str* astr_from_filename(arena* const a, const char* filename) {

    if (a == NULL || filename == NULL) {
        return NULL;
    }

    FILE* file = fopen(filename, "r");
    if (file == NULL) {
        return NULL;
    }

    // str* s = astr_from_file(a, file);
    A_INFO("calling astr_from_file()");
    str* s = astr_from_file(a, file);
    A_INFO("called astr_from_file()");
    // if (s == NULL) { return NULL; } // Removed!

    fclose(file);

    return s;
}

bool str_has_prefix(const str* const s, const char* prefix) {
    if (s == NULL || s->data == NULL || prefix == NULL) {
        return NULL;
    }

    size_t len_prefix = strlen(prefix);
    size_t len_s = str_len(s);

    if (len_prefix > len_s) {
        return false;
    }

    str view = str_view(s, 0, len_prefix);

    bool has_prefix = str_cmp_raw(&view, prefix);

    return has_prefix;
}

bool str_has_suffix(const str* const s, const char* suffix) {
    if (s == NULL || s->data == NULL || suffix == NULL) {
        return NULL;
    }

    size_t len_suffix = strlen(suffix);
    size_t len_s = str_len(s);

    if (len_suffix > len_s) {
        return false;
    }

    str view = str_view(s, len_s - len_suffix, len_s);

    bool has_suffix = str_cmp_raw(&view, suffix);

    return has_suffix;
}

bool str_contains(const str* const s, const char c) {
    if (s == NULL || s->data == NULL) {
        return NULL;
    }
}

str_result str_index_of(const str* const s, const char c) {
    if (s == NULL || s->data == NULL) {
        return (str_result){ .type = SRT_INVALID_PARAMS, .valid = false, .data.index = 0 };
    }

    for (index_t i = 0; i < str_len(s); ++i) {
        if (s->data[i] == c) {
            return (str_result){ .type = SRT_FOUND, .valid = true, .data.index = i };
        }
    }
    return (str_result){ .type = SRT_NOT_FOUND, .valid = true, .data.index = 0 };
}

// TODO: Make this variadic.
void str_print(const char* prefix, const str* const s) {
    if (s != NULL) {
        printf("%s'%.*s'", prefix, (int)s->length, s->data);
    }
}

bool str_valid(const str* s) {
    if (s == NULL) {
        return false;
    }
    if (s->data == NULL) {
        return false;
    }
    if (s->location == AL_UNKNOWN) {
        return false;
    }
    return true;
}

////////// END OF LIBRARY FUNCTIONS //////////

index_t* str_get_alphanumeric_symbolic_boundaries(const str* const s) {
    if (s == NULL || s->data == NULL) {
        return NULL;
    }

    size_t length = 0;
    size_t capacity = 8;
    index_t* boundaries = calloc(capacity, sizeof(*boundaries));
    if (boundaries == NULL) {
        return NULL;
    }

    // Set the first entry to 0
    boundaries[length++] = 0;

    bool is_alpha = isalnum(s->data[0]);
    bool was_alpha = is_alpha;

    size_t len = str_len(s);
    for (size_t index = 1; index < len; index++) {

        // Update state
        char c = s->data[index];
        is_alpha = isalnum(c) || (c == '_');

        // Did the state change between the current position and the previous
        // position? Or is this currently NOT an alphanumeric character?
        if ((is_alpha != was_alpha) || (!is_alpha)) {

            // Expand the boundary list if needed
            if (length == capacity) {
                capacity *= 2;
                void* new_boundaries = realloc(boundaries, capacity * sizeof(*boundaries));
                if (new_boundaries == NULL) {
                    free(boundaries);
                    return NULL;
                }
                boundaries = new_boundaries;
            }

            boundaries[length++] = index;
        }

        was_alpha = is_alpha;
    }

    // Expand the boundary list if needed
    // TODO: Refactor so this is a generic function!
    if (length == capacity) {
        capacity *= 2;
        void* new_boundaries = realloc(boundaries, capacity * sizeof(*boundaries));
        if (new_boundaries == NULL) {
            return NULL;
        }
        boundaries = new_boundaries;
    }

    // Add the final index!
    boundaries[length++] = len;

    return boundaries;
}

bool str_is_identifier(const str* const s) {
    if (s == NULL || s->data == NULL) {
        return NULL;
    }

    size_t len = str_len(s);

    if (len == 0) {
        return false;
    }
    if (!isalpha(s->data[0])) {
        return false;
    }

    for (size_t index = 1; index < len; index++) {
        const char c = s->data[index];
        if (!(isalnum(c) || c == '_')) {
            return false;
        }
    }

    return true;
}

bool str_is_bool_literal(const str* const s) {
    if (s == NULL || s->data) {
        return false;
    }
    return str_cmp_raw(s, "false") || str_cmp_raw(s, "False") || str_cmp_raw(s, "true") || str_cmp_raw(s, "True");
}

bool str_is_u8_literal(const str* const s) {

    if (s == NULL || s->data == NULL) {
        return false;
    }

    const char* suffix = "u8";
    const size_t suffix_len = strlen(suffix);
    const size_t min_number_len = strlen("0");
    const size_t max_number_len = strlen("255");

    // must contain at least one digit; "u8" is not valid => min length is 3
    // cannot contain more than 3 digits + "u8" => max length is 5
    size_t len = str_len(s);
    if (len < (min_number_len + suffix_len) || len > (max_number_len + suffix_len)) {
        return false;
    }

    if (!str_has_suffix(s, suffix)) {
        return false;
    }

    str_result res = str_index_of(s, '-');
    if (res.valid && res.type == SRT_FOUND) {
        return false;
    }

    str view = str_view(s, 0, len - suffix_len);
    if (view.data == NULL) {
        return false;
    }

    char* buffer;
    long value = strtol(view.data, &buffer, 10); // TODO: Add more error checking on this function!

    return (value >= 0 && value <= 255);
}

bool str_is_u16_literal(const str* const s) {
    if (s == NULL || s->data == NULL) {
        return false;
    }

    const char* suffix = "u16";
    const size_t suffix_len = strlen(suffix);
    const size_t min_number_len = strlen("0");
    const size_t max_number_len = strlen("65535");

    // must contain at least one digit; "u16" is not valid => min length is 4
    // cannot contain more than 5 digits + "u16" => max length is 8
    size_t len = str_len(s);
    if (len < (min_number_len + suffix_len) || len > (max_number_len + suffix_len)) {
        return false;
    }

    if (!str_has_suffix(s, suffix)) {
        return false;
    }

    str_result res = str_index_of(s, '-');
    if (res.valid && res.type == SRT_FOUND) {
        return false;
    }

    str view = str_view(s, 0, len - suffix_len);
    if (view.data == NULL) {
        return false;
    }

    char* buffer;
    long value = strtol(view.data, &buffer, 10); // TODO: Add more error checking on this function!

    return (value >= 0 && value <= 65535);
}

bool str_is_u32_literal(const str* const s) {
    if (s == NULL || s->data == NULL) {
        return false;
    }

    const char* suffix = "u32";
    const size_t suffix_len = strlen(suffix);
    const size_t min_number_len = strlen("0");
    const size_t max_number_len = strlen("4294967295");

    // must contain at least one digit; "u32" is not valid => min length is 4
    // cannot contain more than 10 digits + "u32" => max length is 13
    size_t len = str_len(s);
    if (len < (min_number_len + suffix_len) || len > (max_number_len + suffix_len)) {
        return false;
    }

    if (!str_has_suffix(s, suffix)) {
        return false;
    }

    str_result res = str_index_of(s, '-');
    if (res.valid && res.type == SRT_FOUND) {
        return false;
    }

    str view = str_view(s, 0, len - suffix_len);
    if (view.data == NULL) {
        return false;
    }

    char* buffer;
    long value = strtol(view.data, &buffer, 10); // TODO: Add more error checking on this function!

    return (value >= 0L && value <= 4294967295L);
}

bool str_is_u64_literal(const str* const s) {
    if (s == NULL || s->data == NULL) {
        return false;
    }

    const char* suffix = "u64";
    const size_t suffix_len = strlen(suffix);
    const size_t min_number_len = strlen("0");
    const size_t max_number_len = strlen("18446744073709551615");

    // must contain at least one digit; "u64" is not valid => min length is 4
    // cannot contain more than 20 digits + "u64" => max length is 23
    size_t len = str_len(s);
    if (len < (min_number_len + suffix_len) || len > (max_number_len + suffix_len)) {
        return false;
    }

    if (!str_has_suffix(s, suffix)) {
        return false;
    }

    str_result res = str_index_of(s, '-');
    if (res.valid && res.type == SRT_FOUND) {
        return false;
    }

    str view = str_view(s, 0, len - suffix_len);
    if (view.data == NULL) {
        return false;
    }

    char* buffer;
    long value = strtol(view.data, &buffer, 10); // TODO: Add more error checking on this function!

    return (value >= 0UL && value <= 18446744073709551615UL);
}

bool str_is_i8_literal(const str* const s) {
    if (s == NULL || s->data == NULL) {
        return false;
    }

    char* buffer;
    long value = strtol(s->data, &buffer, 10);

    return (value >= -128 && value <= 127);
}

bool str_is_i16_literal(const str* const s) {
    if (s == NULL || s->data == NULL) {
        return false;
    }

    char* buffer;
    long value = strtol(s->data, &buffer, 10);

    return (value >= -32768 && value <= 32767);
}

bool str_is_i32_literal(const str* const s) {
    if (s == NULL || s->data == NULL) {
        return false;
    }

    char* buffer;
    long value = strtol(s->data, &buffer, 10);

    return (value >= -2147483648L && value <= 2147483647L);
}

bool str_is_i64_literal(const str* const s) {
    if (s == NULL || s->data == NULL) {
        return false;
    }

    char* buffer;
    long value = strtol(s->data, &buffer, 10);

    return (value >= -9223372036854775807L && value <= 9223372036854775807L);
}

bool str_is_char_literal(const str* const s) {
    if (s == NULL || s->data == NULL) {
        return false;
    }

    size_t len = str_len(s);

    // ' ? '
    if ((len == 3) && (s->data[0] == '\'') && (s->data[1] != '\'') && (s->data[2] == '\'')) {
        return true;
    }

    // ' \ ? '
    if ((len == 4) && (s->data[0] == '\'') && (s->data[1] == '\\') && (s->data[2] != '\'') && (s->data[3] == '\'')) {
        return true;
    }

    return false;
}

// TODO: FIX THIS FUNCTION; IT SUCKS!!!!
// TODO: this requires a more general solution!
bool str_to_integer_value(const str* const s, uint64_t* value) {

    // Work backward; ignore the last TWO bytes as those will be u8 <-- STUPID
    // ASSUMPTION
    index_t n = s->length - 2;
    for (index_t i = n; i > 0; i--) {
        char digit = s->data[i - 1];

        if (!isdigit(digit))
            return false;

        *value += ((digit - '0') * ipow(10, n - i));
    }

    return true;
}

// TODO: Improve/implement overflow error handling!
bool str_to_u8(const str* const s, uint8_t* value) {
    if (!s) {
        return false;
    }
    if (!value) {
        return false;
    }
    if (!s->data) {
        return false;
    }

    size_t len = str_len(s);
    if (len == 0) {
        return false;
    }

    // No negative values
    if (s->data[0] == '-') {
        return false;
    }

    // "255u8" is the longest possible value; reject everything larger
    if (len > 5) {
        return false;
    }

    int i = 0;
    uint16_t temp_value = 0;
    while (s->data[i] && (s->data[i] >= '0' && s->data[i] <= '9')) {
        temp_value = (temp_value * 10) + (s->data[i] - '0');
        i++;
    }

    *value = temp_value;
    return true;
}

bool str_to_u16(const str* const s, uint16_t* value) {
    if (!s) {
        return false;
    }
    if (!value) {
        return false;
    }
    if (!s->data) {
        return false;
    }

    size_t len = str_len(s);
    if (len == 0) {
        return false;
    }

    // No negative values
    if (s->data[0] == '-') {
        return false;
    }

    // "65_535u16" is the longest possible value; reject everything larger
    if (len > 9) {
        return false;
    }

    int i = 0;
    uint32_t temp_value = 0;
    while (s->data[i] && (s->data[i] >= '0' && s->data[i] <= '9')) {
        temp_value = (temp_value * 10) + (s->data[i] - '0');
        i++;
    }

    *value = temp_value;
    return true;
}

bool str_to_u32(const str* const s, uint32_t* value) {
    if (!s) {
        return false;
    }
    if (!value) {
        return false;
    }
    if (!s->data) {
        return false;
    }

    size_t len = str_len(s);
    if (len == 0) {
        return false;
    }

    // No negative values
    if (s->data[0] == '-') {
        return false;
    }

    // "4_294_967_295u32" is the longest possible value; reject everything
    // larger
    if (len > 16) {
        return false;
    }

    int i = 0;
    uint64_t temp_value = 0;
    while (s->data[i] && (s->data[i] >= '0' && s->data[i] <= '9')) {
        temp_value = (temp_value * 10) + (s->data[i] - '0');
        i++;
    }

    *value = temp_value;

    return true;
}

bool str_to_u64(const str* const s, uint64_t* value) {
    if (!s) {
        return false;
    }
    if (!value) {
        return false;
    }
    if (!s->data) {
        return false;
    }

    size_t len = str_len(s);
    if (len == 0) {
        return false;
    }

    // No negative values
    if (s->data[0] == '-') {
        return false;
    }

    // "18_446_744_073_709_551_616u64" is the longest possible value; reject
    // everything larger
    if (len > 29) {
        return false;
    }

    uint64_t curr_value = 0;
    uint64_t prev_value = 0;

    int i = 0;
    while (s->data[i] && (s->data[i] >= '0' && s->data[i] <= '9')) {

        curr_value = (curr_value * 10) + (s->data[i] - '0');

        if (curr_value < prev_value) {
            return false; // TODO: Make better error handling for
                          // unrepresentable numbers!
        }

        prev_value = curr_value;
        i++;
    }

    *value = curr_value;

    return true;
}

bool str_to_i8(const str* const s, int8_t* value) {
    if (!s) {
        return false;
    }
    if (!value) {
        return false;
    }
    if (!s->data) {
        return false;
    }

    size_t len = str_len(s);
    if (len == 0) {
        return false;
    }

    int8_t sign = 1;
    if (s->data[0] == '-') {
        sign = -1;
    }

    // "-127i8" is the longest possible value; reject everything larger
    if (len > 6) {
        return false;
    }

    int i = 0;
    int16_t temp_value = 0;
    while (s->data[i] && (s->data[i] >= '0' && s->data[i] <= '9')) {
        temp_value = (temp_value * 10) + (s->data[i] - '0');
        i++;
    }

    *value = sign * temp_value;

    return true;
}

bool str_to_i16(const str* const s, int16_t* value) {
    if (!s) {
        return false;
    }
    if (!value) {
        return false;
    }
    if (!s->data) {
        return false;
    }

    size_t len = str_len(s);
    if (len == 0) {
        return false;
    }

    int16_t sign = 1;
    if (s->data[0] == '-') {
        sign = -1;
    }

    // "-32_768i16" is the longest possible value; reject everything larger
    if (len > 10) {
        return false;
    }

    int i = 0;
    int16_t temp_value = 0;
    while (s->data[i] && (s->data[i] >= '0' && s->data[i] <= '9')) {
        temp_value = (temp_value * 10) + (s->data[i] - '0');
        i++;
    }

    *value = sign * temp_value;
    return true;
}

bool str_to_i32(const str* const s, int32_t* value) {
    if (!s) {
        return false;
    }
    if (!value) {
        return false;
    }
    if (!s->data) {
        return false;
    }

    size_t len = str_len(s);
    if (len == 0) {
        return false;
    }

    int32_t sign = 1;
    if (s->data[0] == '-') {
        sign = -1;
    }

    // "-2_147_483_648i32" is the longest possible value; reject everything
    // larger
    if (len > 17) {
        return false;
    }

    int i = 0;
    int32_t temp_value = 0;
    while (s->data[i] && (s->data[i] >= '0' && s->data[i] <= '9')) {
        temp_value = (temp_value * 10) + (s->data[i] - '0');
        i++;
    }

    *value = sign * temp_value;
    return true;
}

bool str_to_i64(const str* const s, int64_t* value) {
    if (!s) {
        return false;
    }
    if (!value) {
        return false;
    }
    if (!s->data) {
        return false;
    }

    size_t len = str_len(s);
    if (len == 0) {
        return false;
    }

    int64_t sign = 1;
    if (s->data[0] == '-') {
        sign = -1;
    }

    // "-9_223_372_036_854_775_808i64" is the longest possible value; reject
    // everything larger
    if (len > 29) {
        return false;
    }

    int i = 0;
    int64_t temp_value = 0;
    while (s->data[i] && (s->data[i] >= '0' && s->data[i] <= '9')) {
        temp_value = (temp_value * 10) + (s->data[i] - '0');
        i++;
    }

    *value = sign * temp_value;
    return true;
}
