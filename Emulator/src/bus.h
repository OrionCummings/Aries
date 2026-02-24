#ifndef BUS_H
#define BUS_H

#include "defs.h"

// TODO: There could be a mechanism to encode input/output/bidirectional bits!

typedef union {
    struct {
        u8 b0 : 1;
        u8 b3 : 1;
        u8 : 6;
    } bits;
    u8 byte;
} bus2_t;

typedef union {
    struct {
        u8 b0 : 1;
        u8 b1 : 1;
        u8 b2 : 1;
        u8 b3 : 1;
        u8 : 4;
    } bits;
    u8 byte;
} bus4_t;

typedef union {
    struct {
        u8 b0 : 1;
        u8 b1 : 1;
        u8 b2 : 1;
        u8 b3 : 1;
        u8 b4 : 1;
        u8 b5 : 1;
        u8 b6 : 1;
        u8 b7 : 1;
    } bits;
    u8 byte;
} bus8_t;

typedef union {
    struct {
        u16 bit0 : 1;
        u16 bit1 : 1;
        u16 bit2 : 1;
        u16 bit3 : 1;
        u16 bit4 : 1;
        u16 bit5 : 1;
        u16 bit6 : 1;
        u16 bit7 : 1;
        u16 bit8 : 1;
        u16 bit9 : 1;
        u16 bit10 : 1;
        u16 bit11 : 1;
        u16 bit12 : 1;
        u16 bit13 : 1;
        u16 bit14 : 1;
        u16 bit15 : 1;
    } bits;
    struct {
        u16 byte0 : 8;
        u16 byte1 : 8;
    } bytes;
    u16 word;
} bus16_t;

typedef union {
    struct {
        u32 bit0 : 1;
        u32 bit1 : 1;
        u32 bit2 : 1;
        u32 bit3 : 1;
        u32 bit4 : 1;
        u32 bit5 : 1;
        u32 bit6 : 1;
        u32 bit7 : 1;
        u32 bit8 : 1;
        u32 bit9 : 1;
        u32 bit10 : 1;
        u32 bit11 : 1;
        u32 bit12 : 1;
        u32 bit13 : 1;
        u32 bit14 : 1;
        u32 bit15 : 1;
        u32 bit16 : 1;
        u32 bit17 : 1;
        u32 bit18 : 1;
        u32 bit19 : 1;
        u32 bit20 : 1;
        u32 bit21 : 1;
        u32 bit22 : 1;
        u32 bit23 : 1;
        u32 bit24 : 1;
        u32 bit25 : 1;
        u32 bit26 : 1;
        u32 bit27 : 1;
        u32 bit28 : 1;
        u32 bit29 : 1;
        u32 bit30 : 1;
        u32 bit31 : 1;
    } bits;
    struct {
        u32 byte0 : 8;
        u32 byte1 : 8;
        u32 byte2 : 8;
        u32 byte3 : 8;
    } bytes;
    struct {
        u32 word0 : 16;
        u32 word1 : 16;
    } words;
    u32 dword;
} bus32_t;

#endif