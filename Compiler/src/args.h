#ifndef __ARGS_H
#define __ARGS_H

#include <string.h>
#include <stdlib.h>
#include <argp.h>
#include "debug.h"
#include "str.h"

#define DEFAULT_GROUP (0)

typedef struct {
    char* args[2];
    LogLevel log_level;
} CommandLineArguments;

/// @brief Parse a single option.
/// @param key 
/// @param arg 
/// @param state 
/// @return Returns a non-zero error code on failure.
error_t parse_opt(int key, char* arg, struct argp_state* state);

str* parse_arguments(int argc, char** restrict argv);

void set_default_values(CommandLineArguments* args);

#endif