#ifndef __LEXER_H
#define __LEXER_H

#include <ctype.h>
#include <stddef.h>
#include "debug.h"
#include "sym_list.h"

typedef struct {
    str* file_content; // TODO: Should the lexer even have this?
    size_t index;
    SymbolList* sym_list;
} Lexer;

Lexer* lex_new(str* file_contents);

void _lex_free(Lexer* lexer);
#define lex_free(l)                                                            \
do {                                                                         \
    _lex_free(l);                                                              \
    l = NULL;                                                                  \
} while (0)

bool lex(Lexer* lexer);
bool lex_add_symbol(Lexer* const lex, Symbol* sym);
Token lex_buffer_to_token(char token_buffer[MAX_IDENTIFIER_LENGTH]);

/// @brief Returns a list of indices at which alphanumeric-symbolic boundaries occur in `s`. Symbolic character strings will always be split as individual characters. This function is guarenteed to return a monotonic sequence of integers (with the final entry being zero!)
/// 
/// Example: 
/// 
/// `str_get_alphanumeric_symbolic_boundaries("a nice test")` yields `[0, 1, 2, 6, 7, 11]`
/// 
/// [0 -  1] = "a"
/// [1 -  2] = " "
/// [2 -  6] = "nice"
/// [6 -  7] = " "
/// [7 - 11] = "test"
/// 
/// @param s The string to split.
/// @return A pointer to a 0-terminated list of indices.
index_t* str_get_alphanumeric_symbolic_boundaries(const str* const s);

/// @brief Returns true if the given string is a valid identifier. Valid identifiers are of the form [a-zA-Z_][a-zA-Z0-9_]*.
/// @param s A string.
/// @return Returns true if the given string is a valid identifier.
bool str_is_identifier(const str* const s);

/// @brief Determines if `s` is a valid literal.
/// @param s The string to check.
/// @return Returns the token type cooresponding to the literal found. If `s` is not a literal, then the `INVALID` token is returned.
Token str_is_literal(const str* const s);

/// @brief Determines if `s` is a valid boolean literal.
/// @param s The string to check.
/// @return Returns `true` if `s` is a valid boolean literal. Otherwise, returns `false`.
bool str_is_bool_literal(const str* const s);

/// @brief Determines if `s` is a valid unsigned 8-bit int literal.
/// @param s The string to check.
/// @return Returns `true` if `s` is a valid unsigned 8-bit int literal. Otherwise, returns `false`.
bool str_is_u8_literal(const str* const s);

/// @brief Determines if `s` is a valid unsigned 16-bit int literal.
/// @param s The string to check.
/// @return Returns `true` if `s` is a valid unsigned 16-bit int literal. Otherwise, returns `false`.
bool str_is_u16_literal(const str* const s);

/// @brief Determines if `s` is a valid unsigned 32-bit int literal.
/// @param s The string to check.
/// @return Returns `true` if `s` is a valid unsigned 32-bit int literal. Otherwise, returns `false`.
bool str_is_u32_literal(const str* const s);

/// @brief Determines if `s` is a valid unsigned 64-bit int literal.
/// @param s The string to check.
/// @return Returns `true` if `s` is a valid unsigned 64-bit int literal. Otherwise, returns `false`.
bool str_is_u64_literal(const str* const s);

/// @brief Determines if `s` is a valid 8-bit int literal.
/// @param s The string to check.
/// @return Returns `true` if `s` is a valid 8-bit int literal. Otherwise, returns `false`.
bool str_is_i8_literal(const str* const s);

/// @brief Determines if `s` is a valid 16-bit int literal.
/// @param s The string to check.
/// @return Returns `true` if `s` is a valid 16-bit int literal. Otherwise, returns `false`.
bool str_is_i16_literal(const str* const s);

/// @brief Determines if `s` is a valid 32-bit int literal.
/// @param s The string to check.
/// @return Returns `true` if `s` is a valid 32-bit int literal. Otherwise, returns `false`.
bool str_is_i32_literal(const str* const s);

/// @brief Determines if `s` is a valid 64-bit int literal.
/// @param s The string to check.
/// @return Returns `true` if `s` is a valid 64-bit int literal. Otherwise, returns `false`.
bool str_is_i64_literal(const str* const s);

/// @brief Determines if `s` is a valid 32-bit float literal.
/// @param s The string to check.
/// @return Returns `true` if `s` is a valid 32-bit float literal. Otherwise, returns `false`.
bool str_is_f32_literal(const str* const s);

/// @brief Determines if `s` is a valid 32-bit float literal.
/// @param s The string to check.
/// @return Returns `true` if `s` is a valid 32-bit float literal. Otherwise, returns `false`.
bool str_is_f64_literal(const str* const s);

/// @brief Determines if `s` is a valid 64-bit float literal.
/// @param s The string to check.
/// @return Returns `true` if `s` is a valid 64-bit float literal. Otherwise, returns `false`.
bool str_is_char_literal(const str* const s);

/// @brief Determines if `s` is a valid string literal.
/// @param s The string to check.
/// @return Returns `true` if `s` is a valid string literal. Otherwise, returns `false`.
bool str_is_str_literal(const str* const s);

/// @brief Determines if `s` is a valid option literal.
/// @param s The string to check.
/// @return Returns `true` if `s` is a valid option literal. Otherwise, returns `false`.
bool str_is_opt_literal(const str* const s);

/// @brief Determines if `s` is a valid result literal.
/// @param s The string to check.
/// @return Returns `true` if `s` is a valid result literal. Otherwise, returns `false`.
bool str_is_res_literal(const str* const s);

#endif
