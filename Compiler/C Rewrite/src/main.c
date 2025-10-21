#include "debug.h"
#include <stdio.h>

#include "lexer.h"
#include "str.h"

int main(int argc, char **argv) {

    const char *filename =
        "/home/orion/Projects/Aries/Compiler/C Rewrite/code/example1.ari";
    Lexer *lexer = lex_new(2, filename);
    if (!lex(lexer)) {
        A_WARNING("Failed to lex file '%s'", filename);
        return -1;
    }

    lex_free(lexer);

    return 0;
}
