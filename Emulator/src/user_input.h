#ifndef USER_INPUT_H
#define USER_INPUT_H

#include <stdio.h>
#include <termios.h>
#include <unistd.h>
#include <signal.h>
#include <string.h>

#define TERMINAL_KEY_ESC (27)
#define TERMINAL_KEY_ENTER (0x0A)
#define TERMINAL_KEY_SPACE (' ')
#define TERMINAL_KEY_R ('r')
#define TERMINAL_KEY_R_CAP ('R')
#define TERMINAL_KEY_M ('m')
#define TERMINAL_KEY_E ('e')
#define TERMINAL_KEY_H ('h')
#define TERMINAL_KEY_X ('x')
#define TERMINAL_KEY_BSLASH ('/')
#define TERMINAL_KEY_1 ('1')
#define TERMINAL_KEY_2 ('2')
#define TERMINAL_KEY_3 ('3')

// TODO: Extract _nearly_ everything in this module into an independent library!

// typedef enum {
//     CMD_SUCCESS = 0,
//     CMD_INVALID_KEYWORD = 1,
//     CMD_INVALID_NARGS = 2,
//     CMD_INVALID_FUNC = 3,
//     CMD_FAILED_FUNC = 4,
// } command_result;

// typedef command_result(*command_func)(command cmd, ...);

// typedef enum {
//     CMDNA_UNKNOWN = -1,
//     CMDNA_ZERO = 0,
//     CMDNA_ONE = 1,
//     CMDNA_TWO = 2,
// } command_nargs;

// typedef struct {
//     const char* keyword;
//     command_nargs nargs;
//     command_result func;
// } command;

/// @brief Disables terminal cannonical mode so the default newline buffer behavior is disabled. This allows for immediate keyboard feedback without pressing the enter key.
void set_non_canonical_mode();

/// @brief Re-enables cannonical mode so the terminal behaves as expected.
void reset_canonical_mode();

/// @brief A function to be called when SIGINT is generated.
/// @param i unknown
void sigint_handler(int i);

void command_handle();

// int command_process(char* cmd, size_t sz);

#endif