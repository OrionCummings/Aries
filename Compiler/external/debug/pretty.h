#ifndef __PRETTY_H
#define __PRETTY_H

#include <stdarg.h>

#define PRETTY_MESSAGE_BUFFER_SIZE (512)

char get_last(const char* s);
void print_pretty(const char* color_code, const char* color_code_reset, const char* restrict s, ...);

#define print_red(s, ...) print_pretty(ANSI_COLOR_RED, ANSI_COLOR_RESET, (s) __VA_OPT__(,) __VA_ARGS__);
#define print_green(s, ...) print_pretty(ANSI_COLOR_GREEN, ANSI_COLOR_RESET, (s) __VA_OPT__(,) __VA_ARGS__);
#define print_yellow(s, ...) print_pretty(ANSI_COLOR_YELLOW, ANSI_COLOR_RESET, (s) __VA_OPT__(,) __VA_ARGS__);
#define print_blue(s, ...) print_pretty(ANSI_COLOR_BLUE, ANSI_COLOR_RESET, (s) __VA_OPT__(,) __VA_ARGS__);
#define print_magenta(s, ...) print_pretty(ANSI_COLOR_MAGENTA, ANSI_COLOR_RESET, (s), __VA_OPT__(,) __VA_ARGS__);
#define print_cyan(s, ...) print_pretty(ANSI_COLOR_CYAN, ANSI_COLOR_RESET, (s) __VA_OPT__(,) __VA_ARGS__);

#define test_case_header() ("\nExecuting function '%s'...\n", __func__);

#endif