#include <stdio.h>
#include "debug.h"

#include "lexer.h"
#include "str.h"

int main(int argc, char** argv) {

    str* s1 = str_new("missing characte");
    str* s2 = str_append(s1, 'r');

    // const char* filename = "/home/orion/Projects/Aries/Compiler/C Rewrite/code/example1.ari";
    // Lexer* lexer = lex_new(2, filename);
    // if (!lex(lexer)) {
    //     A_WARNING("Failed to lex file '%s'", filename);
    //     return -1;
    // }

    return 0;
}
