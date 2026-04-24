#include "user_input.h"

// static const char* command_keywords[] = {
//     "memset", // memset <address> <value>
//     "memcpy", // memcpy <src> <dest>
// };

// CommandFormat commands[] = {
//     (CommandFormat){.cmd = MEMSET, .nargs = 2},
//     (CommandFormat){.cmd = MEMCPY, .nargs = 2},
// };

void set_non_canonical_mode() {
    // TODO: This is linux-specific; make platform agnostic.
    struct termios term;
    tcgetattr(STDIN_FILENO, &term);
    term.c_lflag &= (tcflag_t)(~(ICANON | ECHO));
    tcsetattr(STDIN_FILENO, TCSANOW, &term);
}

void reset_canonical_mode() {
    // TODO: This is linux-specific; make platform agnostic.
    struct termios term;
    tcgetattr(STDIN_FILENO, &term);
    term.c_lflag |= ICANON | ECHO;
    tcsetattr(STDIN_FILENO, TCSANOW, &term);
}

void sigint_handler(int x) {
    reset_canonical_mode();
}

void command_handle() {
    set_non_canonical_mode();


    printf("/");

    char cmd[256] = { 0 };
    size_t sz = 0;
    while ((c = getchar()) != TERMINAL_KEY_ENTER) {
        if (sz < sizeof(cmd) - 1) {
            cmd[sz++] = (char)(c & 0xFF);
        }
        printf("%c", c);
    }
    printf("\n");

    printf("cmd = '%s'\n", cmd);
    if (strncmp("memset", cmd, strlen("memset")) == 0) {

        u8 stage = 0;

        char* addr_str = 0;
        char* data_str = 0;

        char* t = strtok(cmd, " ");
        while (t != NULL) {

            if (stage == 1) {
                addr_str = t;
            } else if (stage == 2) {
                data_str = t;
            }

            t = strtok(NULL, " ");
            stage++;
        }

        printf("addr_str = %s\n", addr_str);
        printf("data_str = %s\n", data_str);

        char* addr_endptr = NULL;
        char* data_endptr = NULL;
        unsigned long addr_ul = strtoul(addr_str, &addr_endptr, 10); // 32 bits
        unsigned long data_ul = strtoul(data_str, &data_endptr, 10); // 8 bits!

        address_t addr = addr_ul & 0xFFFFFFFF;
        u8 data = data_ul & 0xFF;

        printf("addr = %d\n", addr);
        printf("data = %d\n", data);

    } else if (strncmp("memcpy", cmd, strlen("memcpy")) == 0) {
    } else {
        printf("unknown command '%s'\n", cmd);
    }

    reset_canonical_mode();
}

// int command_process(char* cmd, size_t sz) {
//     if (cmd == NULL) { return -1; }
//     if (sz == 0) { return -1; }

//     if (strncmp("memset", cmd, sz)) {

//     } else if (strncmp("memcpy", cmd, sz)) {

//     } else {
//         printf("unknown command '%s'", cmd);
//     }

//     return 0;
// }
