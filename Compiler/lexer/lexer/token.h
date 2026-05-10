#ifndef __TOKEN_H
#define __TOKEN_H

#include "defs.h"
#include "str.h"

TokenType str_to_token(const str* const s);

/// @brief Determines if `s` is a valid literal.
/// @param s The string to check.
/// @return Returns the token type cooresponding to the literal found. If `s` is
/// not a literal, then the `INVALID` token is returned.
TokenType str_is_literal(const str* const s);

#endif