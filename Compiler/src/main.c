#include "debug.h"
#include <stdio.h>

#include "str.h"
#include "lexer.h"
#include "parser.h"

int main(int argc, char** argv) {

    const char* filename = "/home/orion/Projects/Aries/Compiler/code/example0.ari";

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

    lex_print(lexer);
    
    // Parser* parser = parser_new(lexer->sym_list);
    // Parser* parser = NULL;
    // if (!parse(parser)) {
    //     A_WARNING("Failed to parse file '%s'", filename);
    //     return -2;
    // }

    // parser_print(parser);
    
    lex_free(lexer);
    // parser_free(parser);

    return 0;
}
