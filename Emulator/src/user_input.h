#ifndef USER_INPUT_H
#define USER_INPUT_H

#include <stdio.h>
#include <termios.h>
#include <unistd.h>
#include <signal.h>

#define TERMINAL_KEY_ESC (27)
#define TERMINAL_KEY_SPACE (' ')
#define TERMINAL_KEY_R ('r')
#define TERMINAL_KEY_R_CAP ('R')
#define TERMINAL_KEY_M ('m')
#define TERMINAL_KEY_E ('e')
#define TERMINAL_KEY_H ('h')
#define TERMINAL_KEY_1 ('1')
#define TERMINAL_KEY_2 ('2')
#define TERMINAL_KEY_3 ('3')

/// @brief Disables terminal cannonical mode so the default newline buffer behavior is disabled. This allows for immediate keyboard feedback without pressing the enter key.
void set_non_canonical_mode();

/// @brief Re-enables cannonical mode so the terminal behaves as expected.
void reset_canonical_mode();

/// @brief A function to be called when SIGINT is generated.
/// @param i unknown
void sigint_handler(int i);

#endif