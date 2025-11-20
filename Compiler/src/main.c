#include "debug.h"
#include <stdio.h>

#include "str.h"
#include "lexer.h"
#include "parser.h"
#include "arena.h"
#include "args.h"

int main(int argc, char** argv) {

    // TODO: Make this actually work lol
    // parse_arguments(argc, argv);

    const char* filename = "/home/orion/Projects/Aries/Compiler/code/example0.ari";

    Lexer* lexer = lex_new(filename);
    if (!lex(lexer)) {
        A_WARNING("Failed to lex file '%s'", filename);
        return -1;
    }

    // Extract the symlist from the lexer
    SymbolList* symlist = lexer->sym_list;
    if (symlist == NULL) {
        A_WARNING("null symlist");
        return -1;
    }

    // Free the lexer
    lex_free(lexer);
    A_INFO("freed the lexer");
    
    // Make sure the symbols are still ok (they probably aren't because you missed something)
    sym_list_print(*symlist);
    A_INFO("printed the symlist");
    
    // Free the symbol list
    sym_list_free(symlist);
    A_INFO("freed the symlist");

    return 0;
}
