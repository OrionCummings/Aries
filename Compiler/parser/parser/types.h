#ifndef __TYPES_H
#define __TYPES_H

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

#endif