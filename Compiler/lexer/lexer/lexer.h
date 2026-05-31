#ifndef __LEXER_H
#define __LEXER_H

#include "debug.h"
#include "symlist.h"
#include <ctype.h>
#include <stddef.h>

symlist* lex(const str* file_content);

#endif
