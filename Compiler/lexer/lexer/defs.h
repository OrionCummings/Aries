#ifndef __CONSTANTS_H
#define __CONSTANTS_H

#include <stdint.h>

#define MAX_IDENTIFIER_LENGTH (8)
#define DEREF_SYMBOL(s) ((s != NULL) ? *s : NULL_SYMBOL)
#define NULL_CHAR_LOC ((CharacterLocation){.line = 0, .start = 0, .end = 0})
#define NULL_SYMBOL ((Symbol){.location = NULL_CHAR_LOC, .s = NULL, .t = 0})
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

    KW_OPT,    // opt
    KW_VOID,   // void
    KW_BYTE,   // byte
    KW_STRING, // string
    KW_U8,     // u8
    KW_U16,    // u16
    KW_U32,    // u32
    KW_U64,    // u64
    KW_I8,     // i8
    KW_I16,    // i16
    KW_I32,    // i32
    KW_I64,    // i64
    KW_F32,    // f32
    KW_F64,    // f64
    KW_BOOL,   // bool

    KW_BREAK,    // break
    KW_CASE,     // case
    KW_MUT,      // mut
    KW_CONTINUE, // continue
    KW_DEFAULT,  // default
    KW_ELSE,     // else
    KW_ENUM,     // enum
    KW_FOR,      // for
    KW_IF,       // if
    KW_RETURN,   // return
    KW_SIZEOF,   // sizeof
    KW_STATIC,   // static
    KW_STRUCT,   // struct
    KW_SWITCH,   // switch
    KW_DECL,     // decl
    KW_DEF,      // def
    KW_WHILE,    // while
    KW_OVERLOAD, // overload
    KW_ASM,      // asm
    KW_AS,       // as

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

    [KW_OPT] = "KW_OPT",
    [KW_VOID] = "KW_VOID",
    [KW_BYTE] = "KW_BYTE",
    [KW_STRING] = "KW_STRING",
    [KW_U8] = "KW_U8",
    [KW_U16] = "KW_U16",
    [KW_U32] = "KW_U32",
    [KW_U64] = "KW_U64",
    [KW_I8] = "KW_I8",
    [KW_I16] = "KW_I16",
    [KW_I32] = "KW_I32",
    [KW_I64] = "KW_I64",
    [KW_F32] = "KW_F32",
    [KW_F64] = "KW_F64",
    [KW_BOOL] = "KW_BOOL",
    [KW_BREAK] = "KW_BREAK",
    [KW_CASE] = "KW_CASE",
    [KW_MUT] = "KW_MUT",
    [KW_CONTINUE] = "KW_CONTINUE",
    [KW_DEFAULT] = "KW_DEFAULT",
    [KW_ELSE] = "KW_ELSE",
    [KW_ENUM] = "KW_ENUM",
    [KW_FOR] = "KW_FOR",
    [KW_IF] = "KW_IF",
    [KW_RETURN] = "KW_RETURN",
    [KW_SIZEOF] = "KW_SIZEOF",
    [KW_STATIC] = "KW_STATIC",
    [KW_STRUCT] = "KW_STRUCT",
    [KW_SWITCH] = "KW_SWITCH",
    [KW_DECL] = "KW_DECL",
    [KW_DEF] = "KW_DEF",
    [KW_WHILE] = "KW_WHILE",
    [KW_OVERLOAD] = "KW_OVERLOAD",
    [KW_ASM] = "KW_ASM",
    [KW_AS] = "KW_AS",
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
    [KW_OPT] = "opt",
    [KW_VOID] = "void",
    [KW_BYTE] = "byte",
    [KW_STRING] = "string",
    [KW_U8] = "u8",
    [KW_U16] = "u16",
    [KW_U32] = "u32",
    [KW_U64] = "u64",
    [KW_I8] = "i8",
    [KW_I16] = "i16",
    [KW_I32] = "i32",
    [KW_I64] = "i64",
    [KW_F32] = "f32",
    [KW_F64] = "f64",
    [KW_BOOL] = "bool",
    [KW_BREAK] = "break",
    [KW_CASE] = "case",
    [KW_MUT] = "mut",
    [KW_CONTINUE] = "continue",
    [KW_DEFAULT] = "default",
    [KW_ELSE] = "else",
    [KW_ENUM] = "enum",
    [KW_FOR] = "for",
    [KW_IF] = "if",
    [KW_RETURN] = "return",
    [KW_SIZEOF] = "sizeof",
    [KW_STATIC] = "static",
    [KW_STRUCT] = "struct",
    [KW_SWITCH] = "switch",
    [KW_DECL] = "decl",
    [KW_WHILE] = "while",
    [KW_OVERLOAD] = "overload",
    [KW_ASM] = "asm",
    [KW_AS] = "as",
};

#endif