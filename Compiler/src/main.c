#include "arena.h"
#include "debug.h"
#include "lexer.h"
#include "parser.h"
#include "str.h"
#include <stdio.h>
// #include "args.h"

int main(int argc, char** argv) {

    ///////////////////

    // TODO: Make this actually work lol.
    // TODO2: Make this not suck. Or leak memory.
    // A_INFO("capturing passed file name");
    // str* file_name = parse_arguments(argc, argv);
    // str_print("file name = ", file_name);

    ///////////////////

    const char* filename
        = "/home/orion/Projects/Aries/Compiler/code/parser2.ari";
    str* file_content = str_from_filename(filename);

    SymbolList* symlist = lex(file_content);
    if (symlist == NULL) {
        A_WARNING("failed to lex file '%s'", filename);
    }

    // Free the file string
    str_free(file_content);

    // Make sure the symbols are still ok
    symlist_print(*symlist);

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
    // Expression* e = expression_parse(parsing_arena, symlist);
    Expression* e = expression_new(parsing_arena, symlist, 0, symlist->length);
    if (e == NULL) {
        A_WARNING("temp: failed to parse expression from symlist");
    } else {

        Expression* expected = arena_alloc(parsing_arena, sizeof(*expected));
        expected->type = EXPRESSION_T_BIN_OP_ADD;
        expected->value = astr_new(parsing_arena, "9 + 20");

        expected->left = arena_alloc(parsing_arena, sizeof(*expected->left));
        expected->left->left = nullptr;
        expected->left->right = nullptr;
        expected->left->type = EXPRESSION_T_LIT_U8; // BUG: This gets written
                                                    // to expected->value[1]???
        expected->left->value = astr_new(parsing_arena, "9");

        expected->right = arena_alloc(parsing_arena, sizeof(*expected->right));
        expected->right->left = nullptr;
        expected->right->right = nullptr;
        expected->right->type = EXPRESSION_T_LIT_U8;
        expected->right->value = astr_new(parsing_arena, "20");

        print_cyan("\nExpected expression: \n");
        expression_print(*expected, 0);
        print_cyan("\nActual expression: \n");
        expression_print(*e, 0);
        print_cyan("\n");
    }

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
