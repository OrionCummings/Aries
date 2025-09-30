#include <stdio.h>
#include "debug.h"

#include "lexer.h"
#include "str.h"

int main(int argc, char** argv) {

    const char* text = "this is a test string!";
    const char* sub = "test";
    str* s1 = str_new(text);
    str* s2 = str_new(sub);
    int expected_index = 9;

    int actual_index = str_sub(s1, s2);

    str_free(s1);

    // const char* filename = "/home/orion/Projects/Aries/Compiler/C Rewrite/code/example1.ari";
    // Lexer* lexer = lex_new(2, filename);
    // if (!lex(lexer)) {
    //     A_WARNING("Failed to lex file '%s'", filename);
    //     return -1;
    // }

    return 0;
}
