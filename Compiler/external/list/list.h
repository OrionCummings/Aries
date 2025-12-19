#ifndef __LIST_H
#define __LIST_H

#include "debug.h"

#define LIST_DEFAULT_CAPACITY (256)
#define LIST_DEFAULT_GROWTH_FACTOR (2)

/// @cite: https://nachtimwald.com/2020/04/09/generic-list-in-c/

struct list;
typedef struct list list_t;

typedef bool (*list_equal_f)(const void*, const void*);
typedef void* (*list_copy_f)(void*);
typedef void (*list_free_f)(void*);

typedef struct {
    list_equal_f equal;
    list_copy_f copy;
    list_free_f free;
} list_callbacks_t;

typedef enum {
    UCHAR,
    U8,
    U16,
    U32,
    U64,
    I8,
    I16,
    I32,
    I64,
    F32,
    F64,
} list_var_t;

bool list_new(list_t**, list_callbacks_t*);
void list_free(list_t*);

bool list_len(const list_t*, size_t*);

bool list_append(list_t*, void*);
bool list_insert(list_t*, void*, size_t);
bool list_remove(list_t*, size_t index);

bool list_index(const list_t*, const void*, size_t*);
void* list_get(const list_t* size_t);

bool list_to_string(const list_t*, char*, list_var_t);
void list_print(const list_t*, list_var_t);

struct list {
    void** elements;
    size_t size;
    size_t capacity;
    list_callbacks_t callbacks;
};

#endif