#ifndef DECODER_H
#define DECODER_H

#include <stdint.h>
#include <stddef.h>

typedef struct {
    size_t input_size;
    uint8_t* input;
} decoder;

#endif