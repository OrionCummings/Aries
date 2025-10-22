#ifndef __LEXER_H
#define __LEXER_H

#include "debug.h"
#include "str.h"
#include <ctype.h>
#include <stddef.h>

#define MAX_IDENTIFIER_LENGTH (8)
#define TOKEN_LIST_GROWTH_FACTOR (2)
#define NULL_CHAR_RANGE                                                        \
  ((CharacterRange){.char_start = 0, .char_stop = 0, .line = 0})
#define NULL_SYMBOL ((Symbol){.location = NULL_CHAR_RANGE, .s = NULL, .t = 0})
#define DEREF_SYMBOL(s) ((s != NULL) ? *s : NULL_SYMBOL)

typedef enum {
    INVALID, // Used for internal errors
    NONE,
    IDENTIFIER,

    SYM_SPACE,
    SYM_NEWLINE,
    SYM_SEMICOLON,     // ;
    SYM_COLON,         // :
    SYM_COMMA,         // ,
    SYM_QUESTION,      // ?
    SYM_FSLASH,        // /
    SYM_BSLASH,        //
    SYM_PAREN_OPEN,    // (
    SYM_PAREN_CLOSE,   // )
    SYM_BRACKET_OPEN,  // [
    SYM_BRACKET_CLOSE, // ]
    SYM_BRACE_OPEN,    // {
    SYM_BRACE_CLOSE,   // }
    SYM_EQUAL,         // =
    SYM_PLUS,          // +
    SYM_DASH,          // -
    SYM_STAR,          // *
    SYM_PERCENT,       // %
    SYM_EXCLAIM,       // !
    SYM_LT,            // <
    SYM_GT,            // >
    SYM_AMPERSAND,     // &
    SYM_PIPE,          // |
    SYM_CARET,         // ^
    SYM_SQUOTE,        // '
    SYM_DQUOTE,        // "

    LIT_BOOL,   // [t|T]rue | [f|F]alse
    LIT_I8,     //
    LIT_I16,    //
    LIT_I32,    //
    LIT_I64,    //
    LIT_U8,     //
    LIT_U16,    //
    LIT_U32,    //
    LIT_U64,    //
    LIT_F32,    //
    LIT_F64,    //
    LIT_BYTE,   //
    LIT_STRING, // "..."

    KEYWORD_OPT,    // opt
    KEYWORD_VOID,   // void
    KEYWORD_BYTE,   // byte
    KEYWORD_STRING, // string
    KEYWORD_U8,     // u8
    KEYWORD_U16,    // u16
    KEYWORD_U32,    // u32
    KEYWORD_U64,    // u64
    KEYWORD_I8,     // i8
    KEYWORD_I16,    // i16
    KEYWORD_I32,    // i32
    KEYWORD_I64,    // i64
    KEYWORD_F32,    // f32
    KEYWORD_F64,    // f64
    KEYWORD_BOOL,     // bool

    KEYWORD_BREAK,    // break
    KEYWORD_CASE,     // case
    KEYWORD_MUT,      // mut
    KEYWORD_CONTINUE, // continue
    KEYWORD_DEFAULT,  // default
    KEYWORD_ELSE,     // else
    KEYWORD_ENUM,     // enum
    KEYWORD_FOR,      // for
    KEYWORD_IF,       // if
    KEYWORD_RETURN,   // return
    KEYWORD_SIZEOF,   // sizeof
    KEYWORD_STATIC,   // static
    KEYWORD_STRUCT,   // struct
    KEYWORD_SWITCH,   // switch
    KEYWORD_DEF,      // def
    KEYWORD_WHILE,    // while
    KEYWORD_OVERLOAD, // overload
    KEYWORD_ASM,      // asm
    KEYWORD_AS,       // as

    TOKEN_COUNT
} Token;

typedef struct {
    uint16_t line;
    uint16_t char_start;
    uint16_t char_stop;
} CharacterRange;

typedef struct {
    CharacterRange location;
    Token t;
    str* s;
} Symbol;

typedef struct {
    FILE* file;
    size_t index;

    size_t symbol_capacity;
    size_t symbol_length;
    Symbol** symbols;

} Lexer;

bool lex(Lexer* lexer);
Lexer* lex_new(size_t capacity, const char* filename);

void _lex_free(Lexer* lexer);
#define lex_free(l)                                                            \
  do {                                                                         \
    _lex_free(l);                                                              \
    l = NULL;                                                                  \
  } while (0)

bool lex_add_symbol(Lexer* const lex, Symbol* sym);

Token lex_buffer_to_token(char token_buffer[MAX_IDENTIFIER_LENGTH]);

Token str_to_token(const str* const s);
Token str_is_literal(const str* const s);

Symbol* sym_new(const str* const s);
void _sym_free(Symbol*);
#define sym_free(s)                                                            \
do {                                                                         \
    _sym_free(s);                                                              \
    s = NULL;                                                                  \
} while (0)

bool sym_cmp(const Symbol s1, const Symbol s2);
void sym_print(const Symbol);

/// @brief Returns a list of indices at which alphanumeric-symbolic boundaries occur in `s`. Symbolic character strings will always be split as individual characters.
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

/// @brief Returns true if the given string is a valid identifier. Valid identifiers are of the form [a-zA-Z][a-zA-Z0-9_]*.
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
