#ifndef __DEBUG_H
#define __DEBUG_H

#define __STDC_FORMAT_MACROS
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <string.h>
#include <assert.h>
#include <stdbool.h>
#include "colors.h"

#define static_assert(condition, message) _Static_assert((condition), message)

// TODO: Figure out if this is better defined in the top-level CMakeLists.txt or here. It's currently defined by cmake as not *every* file will include debug.h.
// #define false (0)
// #define true  (1)

#define __ENABLE_INFO
#define __ENABLE_WARNING
#define __ENABLE_ERROR
#define __ENABLE_TRACE

#define __DEBUG_MESSAGE_BUFFER_SIZE 512

#define A_INFO(X, ...)    __info(   X, __FILE__, __func__, __LINE__ __VA_OPT__(,) __VA_ARGS__)
#define A_WARNING(X, ...) __warning(X, __FILE__, __func__, __LINE__ __VA_OPT__(,) __VA_ARGS__)
#define A_ERROR(X, ...)   __error(  X, __FILE__, __func__, __LINE__ __VA_OPT__(,) __VA_ARGS__)
#define A_TRACE(...)   __trace(__FILE__, __func__, __LINE__)

typedef enum {
    LOG_NONE,
    LOG_ERROR,
    LOG_WARNING,
    LOG_INFO,
    LOG_TRACE,
    LOG_ALL,
} LogLevel;

extern LogLevel current_log_level;
extern LogLevel previous_log_level;
extern bool enable_ansi_color_codes;

void update_log_level(LogLevel level);

/// @brief Determines the lowest log level that is written to stdout.
#define LOG_PUSH(level)                     \
{                                           \
    previous_log_level = current_log_level; \
    current_log_level = level;              \
};

/// @brief Restores the previous log level.
#define LOG_POP()                           \
{                                           \
    current_log_level = previous_log_level; \
};


void __error(const char* message, const char* file, const char* func, const uint64_t line, ...);
void __warning(const char* message, const char* file, const char* func, const uint64_t line, ...);
void __info(const char* message, const char* file, const char* func, const uint64_t line, ...);
void __trace(const char* file, const char* func, const uint64_t line);

static const char* bits[16] = {
    [0] = "0000",[1] = "0001",[2] = "0010",[3] = "0011",
    [4] = "0100",[5] = "0101",[6] = "0110",[7] = "0111",
    [8] = "1000",[9] = "1001",[10] = "1010",[11] = "1011",
    [12] = "1100",[13] = "1101",[14] = "1110",[15] = "1111",
};

void print_byte(uint8_t);
void print_bytes(uint8_t*, size_t);
void print_word(uint16_t);
void print_words(uint16_t*, size_t);
void print_dword(uint32_t);
void print_dwords(uint32_t*, size_t);
void print_qword(uint64_t);
void print_qwords(uint64_t*, size_t);

#endif