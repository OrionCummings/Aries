#include "args.h"

static const char* program_version = "aires compiler 0.2.0";
static const char* program_bug_address = "<bugs@airesproject.org>";
static char doc[] = "Aries Compiler documentation";
static char args_doc[] = "-f [file_name]";

static struct argp_option options[] = {
  {"file_name", 'f',      0, 0,  "The Aries source file (.ari) to be compiled", DEFAULT_GROUP},
  {"verbose",   'v',      0, 0,  "Produce verbose output", DEFAULT_GROUP},
  {"quiet",     'q',      0, 0,  "Don't produce any output", DEFAULT_GROUP },
  {"log level", 'l',  "LOG", 0,  "Omit log messages up to and including the given level {ALL, ERROR, WARNING, INFO, TRACE, NONE}", DEFAULT_GROUP },
  { 0 }
};

static struct argp argp = { options, parse_opt, args_doc, doc, NULL, NULL, NULL };

/* Parse a single option. */
error_t parse_opt(int key, char* arg, struct argp_state* state) {
    /* Get the input argument from argp_parse, which we
       know is a pointer to our arguments structure. */
    struct arguments* arguments = state->input;

    switch (key) {
    case 'q':
    case 's': {
        arguments->silent = 1;
        break;
    }
    case 'v': {
        arguments->verbose = 1;
        break;
    }
    case 'l': {
        if (strncmp(arg, "ALL", strlen("ALL"))) {
            arguments->log_level = LOG_ALL;
        } else if (strncmp(arg, "ERROR", strlen("ERROR"))) {
            arguments->log_level = LOG_ERROR;
        } else if (strncmp(arg, "WARNING", strlen("WARNING"))) {
            arguments->log_level = LOG_WARNING;
        } else if (strncmp(arg, "INFO", strlen("INFO"))) {
            arguments->log_level = LOG_INFO;
        } else if (strncmp(arg, "TRACE", strlen("TRACE"))) {
            arguments->log_level = LOG_TRACE;
        } else if (strncmp(arg, "NONE", strlen("NONE"))) {
            arguments->log_level = LOG_NONE;
        } else {
            arguments->log_level = LOG_ALL;
        }
        break;
    }
    case ARGP_KEY_ARG: {
        if (state->arg_num >= 3) {
            argp_usage(state);
        }

        arguments->args[state->arg_num] = arg;
        break;
    }

    case ARGP_KEY_END: {

        if (state->arg_num == 0) {
            argp_usage(state);
        }
        break;
    }

    default: {
        return ARGP_ERR_UNKNOWN;
    }
    }
    return 0;
}

void parse_arguments(int argc, char** argv) {

    struct arguments arguments;

    /* Default values. */
    arguments.log_level = LOG_ALL;
    arguments.silent = 0;
    arguments.verbose = 0;
    arguments.output_file = "-";

    /* Parse our arguments; every option seen by parse_opt will
       be reflected in arguments. */
    argp_parse(&argp, argc, argv, 0, 0, &arguments);

    printf(
        "ARG1 = %s\n" \
        "ARG2 = %s\n" \
        "OUTPUT_FILE = %s\n" \
        "VERBOSE = %s\nSILENT = %s\n",
        arguments.args[0],
        arguments.args[1],
        arguments.output_file,
        arguments.verbose ? "yes" : "no",
        arguments.silent ? "yes" : "no");

}