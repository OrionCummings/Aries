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

    const char* filename = "/home/orion/Projects/Aries/Compiler/code/parser2.ari";
    str* file_content = str_from_filename(filename);

    symlist* symlist = lex(file_content);
    if (symlist == NULL) {
        A_WARNING("failed to lex file '%s'", filename);
        str_free(file_content);
        return 3749;
    }

    // Free the file string
    str_free(file_content);

    // Make sure the symbols are still ok
    symlist_print(*symlist);

    ///////////////////

    arena* parsing_arena = arena_new(1024, 1); // TODO: Magic number!
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
    Expression* actual = expression_parse(parsing_arena, symlist, 0);
    if (actual == NULL) {
        A_WARNING("temp: failed to parse expression from symlist");
    } else {

        Expression* expected = arena_alloc(parsing_arena, sizeof(*expected));
        expected->type = ET_LIT_U8;
        expected->value = astr_new(parsing_arena, "255u8");
        expected->left = nullptr;
        expected->right = nullptr;

        print_cyan("\nExpected expression: \n");
        expression_print(*expected, 0);
        print_cyan("\nActual expression: \n");
        expression_print(*actual, 0);
        print_cyan("\n");
        printf("Equal? %s\n", ((expression_eq(expected, actual)) ? "true" : "false"));

        // Expression* expected = arena_alloc(parsing_arena, sizeof(*expected));
        // expected->type = ET_BIN_OP_ADD;
        // expected->value = nullptr;

        // expected->left = arena_alloc(parsing_arena, sizeof(*(expected->left)));
        // expected->left->left = arena_alloc(parsing_arena, sizeof(*(expected->left->left)));
        // expected->left->left->type = ET_LIT_U8;
        // expected->left->left->value = astr_new(parsing_arena, "255u8");
        // expected->left->left->left = nullptr;
        // expected->left->left->right = nullptr;

        // expected->left->right = arena_alloc(parsing_arena, sizeof(*(expected->left->right)));
        // expected->left->right->type = ET_LIT_U8;
        // expected->left->right->value = astr_new(parsing_arena, "12u8");
        // expected->left->right->left = nullptr;
        // expected->left->right->right = nullptr;

        // expected->right = arena_alloc(parsing_arena, sizeof(*(expected->right)));
        // expected->right->left = nullptr;
        // expected->right->right = nullptr;
        // expected->right->type = ET_LIT_U8;
        // expected->right->value = astr_new(parsing_arena, "127u8");

        // print_cyan("\nExpected expression: \n");
        // expression_print(*expected, 0);
        // print_cyan("\nActual expression: \n");
        // expression_print(*actual, 0);
        // print_cyan("\n");
        // printf("Equal? %s\n", ((expression_eq(expected, actual)) ? "true" : "false"));
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
