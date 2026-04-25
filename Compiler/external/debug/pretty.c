#include "pretty.h"
#include "colors.h"
#include "stdio.h"
#include "string.h"

char get_last(const char* s) {
    char last = '\0';
    int i = 0;
    while (s[i]) {
        last = s[i++];
    }
    return last;
}

void print_pretty(const char* color_code, const char* color_code_reset, const char* restrict s, ...) {

    va_list args;
    va_start(args, s);

    char buffer[PRETTY_MESSAGE_BUFFER_SIZE] = { 0 };

    int res = -1;
    if (get_last(s) == '\n') {
        char truncated_s[PRETTY_MESSAGE_BUFFER_SIZE] = { 0 };
        (void)strncpy(truncated_s, s, strlen(s) - 1);
        res = snprintf(buffer, PRETTY_MESSAGE_BUFFER_SIZE, "%s%s%s\n", color_code, truncated_s, color_code_reset);
    } else {
        res = snprintf(buffer, PRETTY_MESSAGE_BUFFER_SIZE, "%s%s%s", color_code, s, color_code_reset);
    }

    if (res > PRETTY_MESSAGE_BUFFER_SIZE) {
        printf("META: The following pretty message was longer than %d characters and has been truncated.\n", PRETTY_MESSAGE_BUFFER_SIZE);
    } else if (res == -1) {
        printf("META: The following pretty message contains an encoding error.\n");
    }

    vprintf(buffer, args);
    va_end(args);
}


