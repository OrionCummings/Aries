#include "debug.h"
#include <stdio.h>

// #include "str.h"
// #include "lexer.h"
// #include "parser.h"
// #include "arena.h"
// #include "args.h"
// #include "bloom_filter.h"

int main(int argc, char** argv) {

    A_INFO("called main()");

    // arena* a = arena_new(1024);

    // size_t k = 6;
    // bfilter* f = bfilter_anew(a, k, hash);

    // uint8_t data[10] = {0};
    // hash_object_t obj = {.n_bytes = 10, .bytes = data};

    // bfilter_in(f, obj);
    // bfilter_add(f, obj);
    // bfilter_in(f, obj);

    // arena_free(a);


    ///////////////////

    // TODO: Make this actually work lol.
    // TODO2: Make this not suck. Or leak memory.
    // A_INFO("capturing passed file name");
    // str* file_name = parse_arguments(argc, argv);
    // str_print("file name = ", file_name);

    ///////////////////

    // const char* filename = "/home/orion/Projects/Aries/Compiler/code/example1.ari";
    // str* file_content = str_from_filename(filename);

    // SymbolList* symlist = lex(file_content);
    // if (symlist == NULL) {
    //     A_WARNING("failed to lex file '%s'", filename);
    //     return -1;
    // }

    // // Free the file string
    // str_free(file_content);
    // A_INFO("freed the file content");

    // // Make sure the symbols are still ok (they probably aren't because you missed something)
    // sym_list_print(*symlist);
    // A_INFO("printed the symlist");

    ///////////////////

    // ASTNode* root = parse(symlist);
    // if (root == NULL) {
    //     A_WARNING("failed to parse symlist");
    //     goto failure_parse;
    // }

    // Free the symbol list
// failure_parse:
    // sym_list_free(symlist);
    // A_INFO("freed the symlist");

    // Free the file name argument
    // str_free(file_name);
    // A_INFO("freed the file name");

    return 0;
}
