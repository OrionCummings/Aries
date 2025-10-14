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
  LIT_STRING, //

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
  str *s;
} Symbol;

typedef struct {
  FILE *file;
  size_t index;

  size_t symbol_capacity;
  size_t symbol_length;
  Symbol *symbols;

} Lexer;

bool lex(Lexer *lexer);
Lexer *lex_new(size_t capacity, const char *filename);

void lex_free_(Lexer *lexer);
#define lex_free(l)                                                            \
  do {                                                                         \
    lex_free_(l);                                                              \
    l = NULL;                                                                  \
  } while (0)

Token lex_buffer_to_token(char token_buffer[MAX_IDENTIFIER_LENGTH]);

Symbol *as_symbol(const str *const s);
Token str_to_token(const str *const s);
bool sym_cmp(const Symbol s1, const Symbol s2);

Symbol *sym_new(Token t, const str *const s);
void sym_free_(Symbol *);
#define sym_free(s)                                                            \
  do {                                                                         \
    sym_free_(s);                                                              \
    s = NULL;                                                                  \
  } while (0)

#endif
