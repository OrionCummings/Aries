#ifndef __CONSTANTS_H
#define __CONSTANTS_H

#include <stdint.h>

#define MAX_IDENTIFIER_LENGTH (8)
#define NULL_SYMBOL ((Symbol){.location = NULL_CHAR_LOC, .s = NULL, .t = 0})
#define DEREF_SYMBOL(s) ((s != NULL) ? *s : NULL_SYMBOL)
#define NULL_CHAR_LOC ((CharacterLocation){.line = 0, .start = 0, .end = 0})
#define crange(l, s, e) ((CharacterLocation){.line = l, .start = s, .end = e})

typedef enum {
    TOKEN_INVALID, // Used for internal errors
    TOKEN_NONE,
    TOKEN_IDENTIFIER,

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
    KEYWORD_BOOL,   // bool

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
    KEYWORD_DECL,     // decl
    KEYWORD_WHILE,    // while
    KEYWORD_OVERLOAD, // overload
    KEYWORD_ASM,      // asm
    KEYWORD_AS,       // as

    TOKEN_COUNT
} Token;

typedef struct {
    uint16_t line;
    uint16_t start;
    uint16_t end;
} CharacterLocation;

static const char* const TOKEN_NAMES[] = {
    [TOKEN_INVALID] = "TOKEN_INVALID",
    [TOKEN_NONE] = "TOKEN_NONE",
    [TOKEN_IDENTIFIER] = "TOKEN_IDENTIFIER",
    [SYM_SPACE] = "SYM_SPACE",
    [SYM_NEWLINE] = "SYM_NEWLINE",
    [SYM_SEMICOLON] = "SYM_SEMICOLON",
    [SYM_COLON] = "SYM_COLON",
    [SYM_COMMA] = "SYM_COMMA",
    [SYM_QUESTION] = "SYM_QUESTION",
    [SYM_FSLASH] = "SYM_FSLASH",
    [SYM_BSLASH] = "SYM_BSLASH",
    [SYM_PAREN_OPEN] = "SYM_PAREN_OPEN",
    [SYM_PAREN_CLOSE] = "SYM_PAREN_CLOSE",
    [SYM_BRACKET_OPEN] = "SYM_BRACKET_OPEN",
    [SYM_BRACKET_CLOSE] = "SYM_BRACKET_CLOSE",
    [SYM_BRACE_OPEN] = "SYM_BRACE_OPEN",
    [SYM_BRACE_CLOSE] = "SYM_BRACE_CLOSE",
    [SYM_EQUAL] = "SYM_EQUAL",
    [SYM_PLUS] = "SYM_PLUS",
    [SYM_DASH] = "SYM_DASH",
    [SYM_STAR] = "SYM_STAR",
    [SYM_PERCENT] = "SYM_PERCENT",
    [SYM_EXCLAIM] = "SYM_EXCLAIM",
    [SYM_LT] = "SYM_LT",
    [SYM_GT] = "SYM_GT",
    [SYM_AMPERSAND] = "SYM_AMPERSAND",
    [SYM_PIPE] = "SYM_PIPE",
    [SYM_CARET] = "SYM_CARET",
    [SYM_SQUOTE] = "SYM_SQUOTE",
    [SYM_DQUOTE] = "SYM_DQUOTE",

    [LIT_I8] = "LIT_I8",
    [LIT_I16] = "LIT_I16",
    [LIT_I32] = "LIT_I32",
    [LIT_I64] = "LIT_I64",
    [LIT_U8] = "LIT_U8",
    [LIT_U16] = "LIT_U16",
    [LIT_U32] = "LIT_U32",
    [LIT_U64] = "LIT_U64",
    [LIT_F32] = "LIT_F32",
    [LIT_F64] = "LIT_F64",
    [LIT_BYTE] = "LIT_BYTE",
    [LIT_STRING] = "LIT_STRING",

    [KEYWORD_OPT] = "KEYWORD_OPT",
    [KEYWORD_VOID] = "KEYWORD_VOID",
    [KEYWORD_BYTE] = "KEYWORD_BYTE",
    [KEYWORD_STRING] = "KEYWORD_STRING",
    [KEYWORD_U8] = "KEYWORD_U8",
    [KEYWORD_U16] = "KEYWORD_U16",
    [KEYWORD_U32] = "KEYWORD_U32",
    [KEYWORD_U64] = "KEYWORD_U64",
    [KEYWORD_I8] = "KEYWORD_I8",
    [KEYWORD_I16] = "KEYWORD_I16",
    [KEYWORD_I32] = "KEYWORD_I32",
    [KEYWORD_I64] = "KEYWORD_I64",
    [KEYWORD_F32] = "KEYWORD_F32",
    [KEYWORD_F64] = "KEYWORD_F64",
    [KEYWORD_BOOL] = "KEYWORD_BOOL",
    [KEYWORD_BREAK] = "KEYWORD_BREAK",
    [KEYWORD_CASE] = "KEYWORD_CASE",
    [KEYWORD_MUT] = "KEYWORD_MUT",
    [KEYWORD_CONTINUE] = "KEYWORD_CONTINUE",
    [KEYWORD_DEFAULT] = "KEYWORD_DEFAULT",
    [KEYWORD_ELSE] = "KEYWORD_ELSE",
    [KEYWORD_ENUM] = "KEYWORD_ENUM",
    [KEYWORD_FOR] = "KEYWORD_FOR",
    [KEYWORD_IF] = "KEYWORD_IF",
    [KEYWORD_RETURN] = "KEYWORD_RETURN",
    [KEYWORD_SIZEOF] = "KEYWORD_SIZEOF",
    [KEYWORD_STATIC] = "KEYWORD_STATIC",
    [KEYWORD_STRUCT] = "KEYWORD_STRUCT",
    [KEYWORD_SWITCH] = "KEYWORD_SWITCH",
    [KEYWORD_DECL] = "KEYWORD_DECL",
    [KEYWORD_WHILE] = "KEYWORD_WHILE",
    [KEYWORD_OVERLOAD] = "KEYWORD_OVERLOAD",
    [KEYWORD_ASM] = "KEYWORD_ASM",
    [KEYWORD_AS] = "KEYWORD_AS",
};

static const char* const SYM_CHARS[] = {
    [SYM_SPACE] = " ",
    [SYM_NEWLINE] = "\n",
    [SYM_SEMICOLON] = ";",
    [SYM_COLON] = ":",
    [SYM_COMMA] = ",",
    [SYM_QUESTION] = "?",
    [SYM_FSLASH] = "/",
    [SYM_BSLASH] = "\\",
    [SYM_PAREN_OPEN] = "(",
    [SYM_PAREN_CLOSE] = ")",
    [SYM_BRACKET_OPEN] = "[",
    [SYM_BRACKET_CLOSE] = "]",
    [SYM_BRACE_OPEN] = "{",
    [SYM_BRACE_CLOSE] = "}",
    [SYM_EQUAL] = "=",
    [SYM_PLUS] = "+",
    [SYM_DASH] = "-",
    [SYM_STAR] = "*",
    [SYM_PERCENT] = "%%",
    [SYM_EXCLAIM] = "!",
    [SYM_LT] = "<",
    [SYM_GT] = ">",
    [SYM_AMPERSAND] = "&",
    [SYM_PIPE] = "|",
    [SYM_CARET] = "^",
    [SYM_SQUOTE] = "'",
    [SYM_DQUOTE] = "\"",
    [KEYWORD_OPT] = "opt",
    [KEYWORD_VOID] = "void",
    [KEYWORD_BYTE] = "byte",
    [KEYWORD_STRING] = "string",
    [KEYWORD_U8] = "u8",
    [KEYWORD_U16] = "u16",
    [KEYWORD_U32] = "u32",
    [KEYWORD_U64] = "u64",
    [KEYWORD_I8] = "i8",
    [KEYWORD_I16] = "i16",
    [KEYWORD_I32] = "i32",
    [KEYWORD_I64] = "i64",
    [KEYWORD_F32] = "f32",
    [KEYWORD_F64] = "f64",
    [KEYWORD_BOOL] = "bool",
    [KEYWORD_BREAK] = "break",
    [KEYWORD_CASE] = "case",
    [KEYWORD_MUT] = "mut",
    [KEYWORD_CONTINUE] = "continue",
    [KEYWORD_DEFAULT] = "default",
    [KEYWORD_ELSE] = "else",
    [KEYWORD_ENUM] = "enum",
    [KEYWORD_FOR] = "for",
    [KEYWORD_IF] = "if",
    [KEYWORD_RETURN] = "return",
    [KEYWORD_SIZEOF] = "sizeof",
    [KEYWORD_STATIC] = "static",
    [KEYWORD_STRUCT] = "struct",
    [KEYWORD_SWITCH] = "switch",
    [KEYWORD_DECL] = "decl",
    [KEYWORD_WHILE] = "while",
    [KEYWORD_OVERLOAD] = "overload",
    [KEYWORD_ASM] = "asm",
    [KEYWORD_AS] = "as",
};


#endif