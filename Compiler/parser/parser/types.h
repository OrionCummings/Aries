#ifndef __TYPES_H
#define __TYPES_H

#include "str.h"

typedef enum BuiltinType : char {
    BITYPE_UNKNOWN,
    BITYPE_VOID,
    BITYPE_BOOL,
    BITYPE_U8,
    BITYPE_U16,
    BITYPE_U32,
    BITYPE_U64,
    BITYPE_I8,
    BITYPE_I16,
    BITYPE_I32,
    BITYPE_I64,
    BITYPE_F32,
    BITYPE_F64,
    BITYPE_OPT,
    BITYPE_RES,
    BITYPE_STR,
} BuiltinType;

typedef struct {
    str* name;
    size_t bytes;
} Type;

static inline bool type_eq(Type a, Type b) { return str_cmp(a.name, b.name); }

typedef struct {
    Type types;
    size_t length;
} TypeTable;

#endif