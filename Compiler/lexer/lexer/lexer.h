#ifndef __LEXER_H
#define __LEXER_H

#include <ctype.h>
#include <stddef.h>
#include "debug.h"
#include "symlist.h"

SymbolList* lex(const str* file_content);

#endif
