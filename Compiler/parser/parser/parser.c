#include "parser.h"

ASTNode* parse(const SymbolList* const symlist) {

    if (!symlist_valid(symlist)) {
        A_ERROR("cannot parse an invalid symlist");
        return NULL;
    }

    arena* arena_parser = arena_new(4096); // TODO: Magic number

    for (size_t sym_idx = 0; sym_idx < symlist->length; sym_idx++) {
        Symbol sym = symlist->symbols[sym_idx];



    }

    return false;
}

void astnode_print(const ASTNode* const node) {
    return;
}