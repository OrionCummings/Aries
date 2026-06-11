#ifndef __REGEX_H
#define __REGEX_H

#include "str.h"
#include "symlist.h"

typedef struct {
    str* pattern;
    // x stack;
    index_t index;
} regex;

regex* regex_new(arena* arena, const char* pattern);

bool regex_scan(regex* const regex, const symlist* const symlist);

bool _validate_pattern(const regex* const regex);

#endif