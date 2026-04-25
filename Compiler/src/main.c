#include <stdio.h>
#include "debug.h"
#include "str.h"
#include "lexer.h"
#include "parser.h"
#include "arena.h"
// #include "args.h"

int main(int argc, char** argv) {

    ///////////////////

    // TODO: Make this actually work lol.
    // TODO2: Make this not suck. Or leak memory.
    // A_INFO("capturing passed file name");
    // str* file_name = parse_arguments(argc, argv);
    // str_print("file name = ", file_name);

    ///////////////////

    const char* filename = "/home/orion/Projects/Aries/Compiler/code/parser2.ari";
    str* file_content = str_from_filename(filename);

    SymbolList* symlist = lex(file_content);
    if (symlist == NULL) {
        A_WARNING("failed to lex file '%s'", filename);
    }

    // Free the file string
    str_free(file_content);
    A_INFO("freed the file content");

    // Make sure the symbols are still ok
    symlist_print(*symlist);
    A_INFO("printed the symlist");

    ///////////////////

    arena* parsing_arena = arena_new(4096); // TODO: Magic number!
    if (parsing_arena == NULL) {
        A_WARNING("failed to allocate a parsing arena");
    }

    // DEBUG: TEMP
    // Declaration* s = declaration_parse(parsing_arena, symlist);
    // if (s == NULL) {
    //         A_WARNING("temp: failed to parse declaration from symlist");
    // } else {
    //     declaration_print(*s);
    // }

    // DEBUG: TEMP
    // Expression* e = expr_parse(parsing_arena, symlist);
    // if (e == NULL) {
    //         A_WARNING("temp: failed to parse expr from symlist");
    // } else {
    //     expr_print(*e);
    // }

    // Declaration* root = parse(parsing_arena, symlist);
    // if (root == NULL) {
    //     A_WARNING("failed to parse symlist");
    // } else {
    //     decl_print(*root);
    // }

    symlist_free(symlist);
    A_INFO("freed the symlist");

    arena_free(parsing_arena);
    A_INFO("freed the parsing arena");

    return 0;
}
