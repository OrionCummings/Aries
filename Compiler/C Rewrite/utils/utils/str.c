#include "str.h"

str* str_new(const char* s) {

    if (s == NULL) {
        return NULL;
    }

    str* r = calloc(1, sizeof(*r));

    if (r != NULL) {

        size_t len = strlen(s); // TODO: !

        r->data = calloc(len + 1, sizeof(*(r->data)));

        strncpy(r->data, s, len);

        r->length = len;
        r->heap = true;
    }

    return r;
}

void _str_free(str* s) {

    if (s != NULL && s->heap) {
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

    if (s1 == NULL || s2 == NULL) {
        return false;
    }

    size_t len_s1 = str_len(s1);
    size_t len_s2 = str_len(s2);
    size_t len_min = (len_s1 < len_s2) ? len_s1 : len_s2;
    return (strncmp(s1->data, s2->data, len_min) == 0) ? true : false;
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
    return (s1 != NULL) && (s2 != NULL) && (s1->heap == s2->heap) &&
        (s1->length == s2->length) && (str_cmp(s1, s2));
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
    if (s == NULL || !s->heap || c == '\0') {
        return NULL;
    }

    size_t length = str_len(s);
    char buffer[length + 1];       // null byte
    memset(buffer, 0, length + 1); // null byte

    (void)snprintf(buffer, length + 2, "%s%c", s->data,
        c); // new char + null byte

    return str_new((char*)buffer); // get that nasty array away!!! Yuck!
}

str* str_view(const str* const s, size_t start, size_t end) {
    if (s == NULL || start >= end) { return NULL; }

    size_t len = str_len(s);
    if (len == 0 || start > len || end > len) { return NULL; }

    str* view = calloc(1, sizeof(*view));
    view->heap = false;
    view->length = end - start;
    view->data = s->data + start;
    return view;
}

str* str_copy(const str* const s, size_t start, size_t end) {
    if (s == NULL || start >= end) { return NULL; }

    size_t len = str_len(s);
    if (len == 0 || start > len || end > len) { return NULL; }

    size_t len_substring = end - start;

    char substring[len_substring + 1];
    memset(substring, 0, len_substring + 1);
    memcpy(substring, s->data + start, len_substring);

    return str_new((char*)substring);
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

    char* buffer = calloc(len, sizeof(*buffer) * len);
    if (buffer == NULL) {
        return NULL;
    }
    fread(buffer, 1, len, file);

    str* s = str_new(buffer);
    free(buffer);
    return s;
}

str* str_from_filename(const char* filename) {
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

bool str_has_prefix(const str* const s, const char* prefix) {
    if (s == NULL || s->data == NULL || prefix == NULL) {
        return NULL;
    }

    size_t len_prefix = strlen(prefix);
    size_t len_s = str_len(s);

    if (len_prefix > len_s) {
        return false;
    }

    str* view_s = str_view(s, 0, len_prefix);

    bool has_prefix = str_cmp_raw(view_s, prefix);

    str_free(view_s);

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

    str* view_s = str_view(s, len_s - len_suffix, len_s);

    bool has_suffix = str_cmp_raw(view_s, suffix);

    str_free(view_s);

    return has_suffix;
}

void str_print(const str* const s) {
    if (s != NULL) {
        printf("%.*s\n", (int)s->length, s->data);
    }
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
        is_alpha = isalnum(c);

        // Did the state change between the current position and the previous
        // position? Or is this currently NOT an alphanumeric character?
        if ((is_alpha != was_alpha) || (!is_alpha)) {

            // Expand the boundary list if needed
            if (length == capacity) {
                capacity *= 2;
                void* new_boundaries =
                    realloc(boundaries, capacity * sizeof(*boundaries));
                if (new_boundaries == NULL) {
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
        void* new_boundaries =
            realloc(boundaries, capacity * sizeof(*boundaries));
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

    // must contain at least one digit; "u8" is not valid => min length is 3
    // cannot contain more than 3 digits + "u8" => max length is 5
    size_t len = str_len(s);
    if (len < 3 || len > 5) { return false; }

    // check the suffix
    if (!str_has_suffix(s, "u8")) { return false; }

    str* view = str_view(s, 0, len - 2);

    char* buffer;
    long value = strtol(view->data, &buffer, 10);

    return (value >= 0 && value <= 255);
}

bool str_is_u16_literal(const str* const s) {
    if (s == NULL || s->data == NULL) {
        return false;
    }

    // must contain at least one digit; "u16" is not valid => min length is 4
    // cannot contain more than 5 digits + "u16" => max length is 8
    size_t len = str_len(s);
    if (len < 4 || len > 8) { return false; }

    // check the suffix
    if (!str_has_suffix(s, "u16")) { return false; }

    str* view = str_view(s, 0, len - 3);

    char* buffer;
    long value = strtol(s->data, &buffer, 10);

    return (value >= 0 && value <= 65535);
}

bool str_is_u32_literal(const str* const s) {
    if (s == NULL || s->data == NULL) {
        return false;
    }

    // must contain at least one digit; "u32" is not valid => min length is 4
    // cannot contain more than 10 digits + "u32" => max length is 13
    // u32's are the default type, so it actually CAN have 1 digit!
    size_t len = str_len(s);
    if (len < 1 || len > 13) { return false; }
    if (!isdigit(s->data[0])) { return false; }

    // check the suffix
    str* view = NULL;
    if (str_has_suffix(s, "u32")) {
        view = str_view(s, 0, len - 3);
    } else {
        view = str_view(s, 0, len); // TODO: Remove this; just use s?
    }

    if (view == NULL) { return false; }

    char* buffer;
    long value = strtol(view->data, &buffer, 10);

    int has_suffix = strcmp(buffer, "u32");
    int lacks_suffix = strcmp(buffer, "");
    if (has_suffix != 0 && lacks_suffix != 0) {
        return false;
    }

    return (value >= 0L && value <= 4294967295L);
}

bool str_is_u64_literal(const str* const s) {
    if (s == NULL || s->data == NULL) {
        return false;
    }

    // must contain at least one digit; "u64" is not valid => min length is 4
    // cannot contain more than 20 digits + "u64" => max length is 23
    size_t len = str_len(s);
    if (len < 4 || len > 23) { return false; }

    // check the suffix
    if (!str_has_suffix(s, "u64")) { return false; }

    str* view = str_view(s, 0, len - 3);

    char* buffer;
    long value = strtoul(s->data, &buffer, 10);

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

