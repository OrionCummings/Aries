#ifndef __MAP_H
#define __MAP_H

#include "debug.h"
#include "arena.h"
#include "hash.h"

typedef struct {
    hash_t(*f)(void* data, size_t length);
    size_t size;
    void* data;
} map;

// map* map_anew(const arena* a, );

// bool map_add();

#endif