#ifndef __ARGS_H
#define __ARGS_H

#include <string.h>
#include <stdlib.h>
#include <argp.h>
#include "debug.h"

#define DEFAULT_GROUP (0)

struct arguments {
    char* args[4];
    int silent, verbose;
    LogLevel log_level;
    char* output_file;
};

error_t parse_opt(int key, char* arg, struct argp_state* state);

void parse_arguments(int argc, char** argv);

#endif