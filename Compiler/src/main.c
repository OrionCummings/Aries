#include "debug.h"
#include <stdio.h>

#include "str.h"
#include "lexer.h"
#include "parser.h"
#include "arena.h"
#include "args.h"

int main(int argc, char** argv) {

    // TODO: Make this actually work lol.
    // TODO2: Make this not suck. Or leak memory.
    // A_INFO("capturing passed file name");
    // str* file_name = parse_arguments(argc, argv);
    // str_print("file name = ", file_name);

    const char* filename = "/home/orion/Projects/Aries/Compiler/code/example-1.ari";
    str* file_content = str_from_filename(filename);

    SymbolList* symlist = lex(file_content);
    if (symlist == NULL) {
        A_WARNING("failed to lex file '%s'", filename);
        return -1;
    }

    // Free the file string
    str_free(file_content);
    A_INFO("freed the file content");

    // Make sure the symbols are still ok (they probably aren't because you missed something)
    sym_list_print(*symlist);
    A_INFO("printed the symlist");

    // Free the symbol list
    sym_list_free(symlist);
    A_INFO("freed the symlist");

    // Free the file name argument
    // str_free(file_name);
    // A_INFO("freed the file name");

    return 0;
}
