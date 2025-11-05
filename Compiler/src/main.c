#include "debug.h"
#include <stdio.h>

#include "lexer.h"
#include "str.h"

int main(int argc, char** argv) {

    const char* filename = "/home/orion/Projects/Aries/Compiler/code/example5.ari";

    str* file_content = str_from_filename(filename);
    if (file_content == NULL) {
        A_WARNING("Failed to read file '%s'", filename);
        return -1;
    }

    Lexer* lexer = lex_new(file_content);
    if (!lex(lexer)) {
        A_WARNING("Failed to lex file '%s'", filename);
        return -1;
    }

    lex_free(lexer);

    return 0;
}
