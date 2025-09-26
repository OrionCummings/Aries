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

    if (s != NULL) {
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
    return false;
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

int str_sub(const str* const s1, const str* const s2) {
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

void str_print(const str* const s) {
    if (s != NULL) {
        printf("%s\n", s->data);
    }
}