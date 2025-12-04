#include "args.h"

const char *argp_program_version = "Aires compiler 0.2.0";
static const char* program_bug_address = "<bugs@airesproject.org>";
static char doc[] = "Aries Compiler documentation";
static char args_doc[] = "file";

static struct argp_option options[] = {
  {"log_level", 'l',  "LOG", OPTION_ARG_OPTIONAL,  "Omit log messages up to and including the given level: ALL, ERROR, WARNING, INFO, TRACE, NONE", DEFAULT_GROUP },
  { 0 }
};


static struct argp argp = { options, parse_opt, args_doc, doc, NULL, NULL, NULL };

error_t parse_opt(int key, char* arg, struct argp_state* state) {

    // A_INFO("parsing option");

    CommandLineArguments* arguments = state->input;

    switch (key) {
    case 'l': {
        // A_INFO("parsing -l option");

        if (strncmp(arg, "ALL", strlen("ALL")) == 0) {
            arguments->log_level = LOG_ALL;
        } else if (strncmp(arg, "ERROR", strlen("ERROR")) == 0) {
            arguments->log_level = LOG_ERROR;
        } else if (strncmp(arg, "WARNING", strlen("WARNING")) == 0) {
            arguments->log_level = LOG_WARNING;
        } else if (strncmp(arg, "INFO", strlen("INFO")) == 0) {
            arguments->log_level = LOG_INFO;
        } else if (strncmp(arg, "TRACE", strlen("TRACE")) == 0) {
            arguments->log_level = LOG_TRACE;
        } else if (strncmp(arg, "NONE", strlen("NONE")) == 0) {
            arguments->log_level = LOG_NONE;
        } else {
            arguments->log_level = LOG_ALL;
        }
        break;
    }
    case ARGP_KEY_ARG: {
        // A_INFO("parsing ARGP_KEY_ARG option");

        if (state->arg_num >= 1) {
            argp_usage(state);
        }

        arguments->args[state->arg_num] = arg;
        break;
    }

    case ARGP_KEY_END: {
        // A_INFO("parsing ARGP_KEY_END option");

        if (state->arg_num == 0) {
            argp_usage(state);
        }

        // if (arguments->output_file == NULL){
        //     argp_failure(state, 1, 0, "required -f. See --help for more information");
        //     exit(ARGP_ERR_UNKNOWN);
        // }

        break;
    }

    default: {
        // A_INFO("parsing default option");
        return ARGP_ERR_UNKNOWN;
    }
    }
    return 0;
}

void set_default_values(CommandLineArguments* args) {
    args->log_level = LOG_ALL;
}

str* parse_arguments(int argc, char** restrict argv) {

    CommandLineArguments arguments;
    set_default_values(&arguments);

    argp_parse(&argp, argc, argv, 0, 0, &arguments);
    error_t err = argp_parse(&argp, argc, argv, 0, 0, &arguments);
    if (err) {
        // A_ERROR("failed to parse arguments");
        return NULL;
    }

    update_log_level(arguments.log_level);

    str* s = str_new(arguments.args[0]);
    if (s == NULL || s->data == NULL) {
        // A_ERROR("failed to capture file path argument");
        return NULL;
    }

    return s;
}