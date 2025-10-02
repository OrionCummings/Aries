#include "str.h"

str* str_new(const char* s) {

    if (s == NULL) {
        return NULL;
    }

    str* r = calloc(1, sizeof(*r));

    if (r != NULL) {

        size_t len = strlen(s);

        r->data = calloc(len + 1, sizeof(*(r->data)));

        strcpy(r->data, s);

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

    if (s1 == NULL || s2 == NULL) { return false; }

    size_t len_s1 = str_len(s1);
    size_t len_s2 = str_len(s2);
    size_t len_min = (len_s1 < len_s2) ? len_s1 : len_s2;
    return (strncmp(s1->data, s2->data, len_min) == 0) ? true : false;
}

bool str_ident(const str* const s1, const str* const s2) {
    return (s1 != NULL) && (s2 != NULL) && (s1->heap == s2->heap) && (s1->length == s2->length) && (str_cmp(s1, s2));
}

int str_find(const str* const s, const char c) {

    if (s == NULL) { return -1; }

    for (size_t index = 0; index < str_len(s); index++) {
        if (str_at(s, index) == c) {
            return index;
        }
    }

    return -1;
}

int str_sub(const str* const s, const str* const sub) {

    if (s == NULL || sub == NULL) { return -1; }

    size_t len_s = str_len(s);
    size_t len_sub = str_len(sub);

    // If the length of the sub string is greater than the string, then there is no way for it to be a sub string
    if (len_sub > len_s) { return -1; }

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
    if (s == NULL) { return 0; }

    size_t length = str_len(s);

    if (index > length) { return 0; }

    return s->data[index];
}

str* str_append(const str* const s, const char c) {
    if (s == NULL || !s->heap || c == '\0') { return NULL; }

    size_t length = str_len(s);
    char buffer[length + 1]; // null byte
    memset(buffer, 0, length + 1); // null byte

    (void)snprintf(buffer, length + 2, "%s%c", s->data, c); // new char + null byte

    return str_new((char*)buffer); // get that nasty array away!!! Yuck!
}

str* str_view(const str* const s, size_t start, size_t end) {
    if (s == NULL) { return NULL; }
    if (start >= end) { return NULL; }

    size_t len = str_len(s);
    if (len == 0 || start > len || end > len) { return NULL; }

    size_t len_substring = end - start - 1;
    char substring[len_substring + 1];
    memset(substring, 0, len_substring + 1);
    memcpy(substring, s->data + start, len_substring);

    str* view = str_new((char*)substring);
    view->heap = false;
    return view;
}

index* str_get_alphanumeric_symbolic_boundaries(const str* const s) {

    if (s == NULL) { return NULL; }
    if (s->data == NULL) { return NULL; }

    size_t length = 0;
    size_t capacity = 8;
    index* boundaries = calloc(capacity, sizeof(*boundaries));
    if (boundaries == NULL) { return NULL; }

    // Set the first entry to 0
    boundaries[length++] = 0;

    bool is_alpha = isalnum(s->data[0]);
    bool was_alpha = is_alpha;

    size_t len = str_len(s);
    for (size_t index = 1; index < len; index++) {

        // Update state
        char c = s->data[index];
        is_alpha = isalnum(c);

        // Did the state change between the current position and the previous position?
        if (is_alpha != was_alpha) {

            // Expand the boundary list if needed
            if (length == capacity) {
                capacity *= 2;
                void* new_boundaries = realloc(boundaries, capacity * sizeof(*boundaries));
                if (new_boundaries == NULL) {
                    return NULL;
                }
                boundaries = new_boundaries;
            }

            boundaries[length++] = index;
        }

        // Remember the state
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

char* str_raw(const str* const s) {
    if (s == NULL || s->data == NULL) { return NULL; }

    size_t len_s = str_len(s);
    void* ptr = calloc(len_s + 1, sizeof(char));
    if (ptr == NULL) { return NULL; }

    strncpy(ptr, s->data, len_s);
    return (char*)ptr;
}

void str_print(const str* const s) {
    if (s != NULL) {
        printf("%s\n", s->data);
    }
}

