#include "user_input.h"

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