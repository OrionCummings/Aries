#include "lexer.h"

const char* const SYM_NAMES[] = {
    [SYM_SPACE] = " ",
    [SYM_EOF] = "EOF",
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
    [KEYWORD_CHAR] = "char",
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
    [KEYWORD_DEF] = "def",
    [KEYWORD_WHILE] = "while",
    [KEYWORD_OVERLOAD] = "overload",
    [KEYWORD_ASM] = "asm",
    [KEYWORD_AS] = "as",
};

const char* const TOKEN_NAMES[] = {
    [INVALID] = "INVALID",
    [NONE] = "NONE",
    [IDENTIFIER] = "IDENTIFIER",
    [SYM_EOF] = "SYM_EOF",
    [SYM_SPACE] = " ",
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
    [LIT_INT] = "LIT_INT",
    [LIT_UINT] = "LIT_UINT",
    [LIT_FLOAT] = "LIT_FLOAT",
    [LIT_CHAR] = "LIT_CHAR",
    [LIT_STRING] = "LIT_STRING",
    [KEYWORD_OPT] = "KEYWORD_OPT",
    [KEYWORD_VOID] = "KEYWORD_VOID",
    [KEYWORD_CHAR] = "KEYWORD_CHAR",
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
    [KEYWORD_DEF] = "KEYWORD_DEF",
    [KEYWORD_WHILE] = "KEYWORD_WHILE",
    [KEYWORD_OVERLOAD] = "KEYWORD_OVERLOAD",
    [KEYWORD_ASM] = "KEYWORD_ASM",
    [KEYWORD_AS] = "KEYWORD_AS",
};

bool lex(Lexer* lexer) {

    if (lexer == NULL) { A_WARNING("Passed null parameter 'lexer'"); return false; }

    str* file_contents = str_from_file(lexer->file);
    size_t len = str_len(file_contents);
    index_t* boundaries = str_get_alphanumeric_symbolic_boundaries(file_contents);

    size_t index = 0;
    while (boundaries[index++] != len) {
        index_t start = boundaries[index - 1];
        index_t end = boundaries[index] + 1;

        str* view = str_view(file_contents, start, end);

        Token token = str_to_token(view);

        printf("%s ('%s')\n", TOKEN_NAMES[token], view->data);
    }

    fclose(lexer->file);
    free(lexer->symbols); // TODO: Remove this eventually lol

    return true;
}

Lexer* lex_new(size_t capacity, const char* filename) {

    Lexer* lexer = calloc(1, sizeof(*lexer));
    if (lexer == NULL) {
        A_WARNING("failed to allocate new lexer");
        return false;
    }

    lexer->symbol_capacity = capacity;

    void* symbols = calloc(capacity, sizeof(*lexer->symbols));
    if (symbols == NULL) {
        A_WARNING("failed to allocate new lexer->symbols");
        return false;
    }

    lexer->symbols = symbols;

    FILE* file = fopen(filename, "r");
    if (file == NULL) {
        A_WARNING("Failed to open file '%s'", filename);
        return false;
    }

    A_INFO("Opened file '%s'", filename);

    lexer->file = file;

    return lexer;
}

bool lex_append(Lexer* lexer, Symbol sym) {
    return true;
}

Symbol* as_symbol(const str* const s) {

    if (s == NULL || s->data == NULL) { return NULL; }

    Token t = lex_buffer_to_token(s->data);
    Symbol* sym = sym_new(t, s);

    if (sym == NULL) { return NULL; }

    return sym;
}

bool is_identifier_char(char c) {
    return (isalnum(c) || c == '_');
}

Symbol* sym_new(Token t, const str* const s) {

    if (s == NULL) { return NULL; }

    Symbol* sym = calloc(1, sizeof(Symbol));
    if (sym == NULL) {
        A_WARNING("failed to allocate new symbol");
        return NULL;
    }

    // If it's an identifier, then we DON'T know what the text will
    // be so we save it. If it's NOT an identifier, then it's a keyword
    // or known symbol; save memory and don't track the character content.
    // Regardless, save the token information!
    sym->t = t;
    if (t == IDENTIFIER) {
        sym->s = calloc(str_len(s), sizeof(*sym->s));
        sym->s = str_new(s->data);
        return sym;

    } else {
        sym->s = NULL;
        return sym;

    }
}

void sym_free_(Symbol* s) {
    if (s != NULL) {
        free(s->s);
    }
    free(s);
}

Token str_to_token(const str* const s) {
    if (s == NULL) { return INVALID; }

    for (size_t index = 3; index < TOKEN_COUNT; index++) {
        if (str_cmp_raw(s, SYM_NAMES[index])) {
            return (Token)index;
        }
    }

    if (str_is_identifier(s)) {
        return IDENTIFIER;
    }

    return INVALID;

    /** This obviously sucks, but i typed it out so it's staying for a while
    if (str_cmp_raw(s, TOKEN_NAMES[NONE])) {
        return NONE;
    } else if (str_cmp_raw(s, TOKEN_NAMES[WHITESPACE])) {
        return WHITESPACE;
    } else if (str_cmp_raw(s, TOKEN_NAMES[SYM_EOF])) {
        return SYM_EOF;
    } else if (str_cmp_raw(s, TOKEN_NAMES[SYM_SEMICOLON])) {
        return SYM_SEMICOLON;
    } else if (str_cmp_raw(s, TOKEN_NAMES[SYM_COLON])) {
        return SYM_COLON;
    } else if (str_cmp_raw(s, TOKEN_NAMES[SYM_COMMA])) {
        return SYM_COMMA;
    } else if (str_cmp_raw(s, TOKEN_NAMES[SYM_QUESTION])) {
        return SYM_QUESTION;
    } else if (str_cmp_raw(s, TOKEN_NAMES[SYM_FSLASH])) {
        return SYM_FSLASH;
    } else if (str_cmp_raw(s, TOKEN_NAMES[SYM_BSLASH])) {
        return SYM_BSLASH;
    } else if (str_cmp_raw(s, TOKEN_NAMES[SYM_PAREN_OPEN])) {
        return SYM_PAREN_OPEN;
    } else if (str_cmp_raw(s, TOKEN_NAMES[SYM_PAREN_CLOSE])) {
        return SYM_PAREN_CLOSE;
    } else if (str_cmp_raw(s, TOKEN_NAMES[SYM_BRACKET_OPEN])) {
        return SYM_BRACKET_OPEN;
    } else if (str_cmp_raw(s, TOKEN_NAMES[SYM_BRACKET_CLOSE])) {
        return SYM_BRACKET_CLOSE;
    } else if (str_cmp_raw(s, TOKEN_NAMES[SYM_BRACE_OPEN])) {
        return SYM_BRACE_OPEN;
    } else if (str_cmp_raw(s, TOKEN_NAMES[SYM_BRACE_CLOSE])) {
        return SYM_BRACE_CLOSE;
    } else if (str_cmp_raw(s, TOKEN_NAMES[SYM_EQUAL])) {
        return SYM_EQUAL;
    } else if (str_cmp_raw(s, TOKEN_NAMES[SYM_PLUS])) {
        return SYM_PLUS;
    } else if (str_cmp_raw(s, TOKEN_NAMES[SYM_DASH])) {
        return SYM_DASH;
    } else if (str_cmp_raw(s, TOKEN_NAMES[SYM_STAR])) {
        return SYM_STAR;
    } else if (str_cmp_raw(s, TOKEN_NAMES[SYM_PERCENT])) {
        return SYM_PERCENT;
    } else if (str_cmp_raw(s, TOKEN_NAMES[SYM_EXCLAIM])) {
        return SYM_EXCLAIM;
    } else if (str_cmp_raw(s, TOKEN_NAMES[SYM_LT])) {
        return SYM_LT;
    } else if (str_cmp_raw(s, TOKEN_NAMES[SYM_GT])) {
        return SYM_GT;
    } else if (str_cmp_raw(s, TOKEN_NAMES[SYM_AMPERSAND])) {
        return SYM_AMPERSAND;
    } else if (str_cmp_raw(s, TOKEN_NAMES[SYM_PIPE])) {
        return SYM_PIPE;
    } else if (str_cmp_raw(s, TOKEN_NAMES[SYM_CARET])) {
        return SYM_CARET;
    } else if (str_cmp_raw(s, TOKEN_NAMES[SYM_SQUOTE])) {
        return SYM_SQUOTE;
    } else if (str_cmp_raw(s, TOKEN_NAMES[SYM_DQUOTE])) {
        return SYM_DQUOTE;
    } else if (str_cmp_raw(s, TOKEN_NAMES[LIT_INT])) {
        return LIT_INT;
    } else if (str_cmp_raw(s, TOKEN_NAMES[LIT_UINT])) {
        return LIT_UINT;
    } else if (str_cmp_raw(s, TOKEN_NAMES[LIT_FLOAT])) {
        return LIT_FLOAT;
    } else if (str_cmp_raw(s, TOKEN_NAMES[LIT_CHAR])) {
        return LIT_CHAR;
    } else if (str_cmp_raw(s, TOKEN_NAMES[LIT_STRING])) {
        return LIT_STRING;
    } else if (str_cmp_raw(s, TOKEN_NAMES[KEYWORD_OPT])) {
        return KEYWORD_OPT;
    } else if (str_cmp_raw(s, TOKEN_NAMES[KEYWORD_VOID])) {
        return KEYWORD_VOID;
    } else if (str_cmp_raw(s, TOKEN_NAMES[KEYWORD_CHAR])) {
        return KEYWORD_CHAR;
    } else if (str_cmp_raw(s, TOKEN_NAMES[KEYWORD_STRING])) {
        return KEYWORD_STRING;
    } else if (str_cmp_raw(s, TOKEN_NAMES[KEYWORD_U8])) {
        return KEYWORD_U8;
    } else if (str_cmp_raw(s, TOKEN_NAMES[KEYWORD_U16])) {
        return KEYWORD_U16;
    } else if (str_cmp_raw(s, TOKEN_NAMES[KEYWORD_U32])) {
        return KEYWORD_U32;
    } else if (str_cmp_raw(s, TOKEN_NAMES[KEYWORD_U64])) {
        return KEYWORD_U64;
    } else if (str_cmp_raw(s, TOKEN_NAMES[KEYWORD_I8])) {
        return KEYWORD_I8;
    } else if (str_cmp_raw(s, TOKEN_NAMES[KEYWORD_I16])) {
        return KEYWORD_I16;
    } else if (str_cmp_raw(s, TOKEN_NAMES[KEYWORD_I32])) {
        return KEYWORD_I32;
    } else if (str_cmp_raw(s, TOKEN_NAMES[KEYWORD_I64])) {
        return KEYWORD_I64;
    } else if (str_cmp_raw(s, TOKEN_NAMES[KEYWORD_F32])) {
        return KEYWORD_F32;
    } else if (str_cmp_raw(s, TOKEN_NAMES[KEYWORD_F64])) {
        return KEYWORD_F64;
    } else if (str_cmp_raw(s, TOKEN_NAMES[KEYWORD_BOOL])) {
        return KEYWORD_BOOL;
    } else if (str_cmp_raw(s, TOKEN_NAMES[KEYWORD_BREAK])) {
        return KEYWORD_BREAK;
    } else if (str_cmp_raw(s, TOKEN_NAMES[KEYWORD_CASE])) {
        return KEYWORD_CASE;
    } else if (str_cmp_raw(s, TOKEN_NAMES[KEYWORD_MUT])) {
        return KEYWORD_MUT;
    } else if (str_cmp_raw(s, TOKEN_NAMES[KEYWORD_CONTINUE])) {
        return KEYWORD_CONTINUE;
    } else if (str_cmp_raw(s, TOKEN_NAMES[KEYWORD_DEFAULT])) {
        return KEYWORD_DEFAULT;
    } else if (str_cmp_raw(s, TOKEN_NAMES[KEYWORD_ENUM])) {
        return KEYWORD_ENUM;
    } else if (str_cmp_raw(s, TOKEN_NAMES[KEYWORD_FOR])) {
        return KEYWORD_FOR;
    } else if (str_cmp_raw(s, TOKEN_NAMES[KEYWORD_RETURN])) {
        return KEYWORD_RETURN;
    } else if (str_cmp_raw(s, TOKEN_NAMES[KEYWORD_SIZEOF])) {
        return KEYWORD_SIZEOF;
    } else if (str_cmp_raw(s, TOKEN_NAMES[KEYWORD_STATIC])) {
        return KEYWORD_STATIC;
    } else if (str_cmp_raw(s, TOKEN_NAMES[KEYWORD_STRUCT])) {
        return KEYWORD_STRUCT;
    } else if (str_cmp_raw(s, TOKEN_NAMES[KEYWORD_SWITCH])) {
        return KEYWORD_SWITCH;
    } else if (str_cmp_raw(s, TOKEN_NAMES[KEYWORD_DEF])) {
        return KEYWORD_DEF;
    } else if (str_cmp_raw(s, TOKEN_NAMES[KEYWORD_WHILE])) {
        return KEYWORD_WHILE;
    } else if (str_cmp_raw(s, TOKEN_NAMES[KEYWORD_OVERLOAD])) {
        return KEYWORD_OVERLOAD;
    } else if (str_cmp_raw(s, TOKEN_NAMES[KEYWORD_ASM])) {
        return KEYWORD_ASM;
    } else if (str_cmp_raw(s, TOKEN_NAMES[KEYWORD_AS])) {
        return KEYWORD_AS;
    } else if (str_is_identifier(s)) {
        return IDENTIFIER;
    } else {
        return INVALID;
    }
    //**/
}

Token lex_buffer_to_token(char token_buffer[MAX_IDENTIFIER_LENGTH]) {

    // TODO: Come back here and appreciate how awful this is. Go on. Do it.
    // Refactor it, coward.
    if (token_buffer[0] == EOF) {
        return SYM_EOF;
    } else if (token_buffer[0] == ' ') {
        return SYM_SPACE;
    } else if (token_buffer[0] == '\0') {
        return NONE;
    } else if (token_buffer[0] == ';') {
        return SYM_SEMICOLON;
    } else if (token_buffer[0] == ':') {
        return SYM_COLON;
    } else if (token_buffer[0] == ',') {
        return SYM_COMMA;
    } else if (token_buffer[0] == '?') {
        return SYM_QUESTION;
    } else if (token_buffer[0] == '/') {
        return SYM_FSLASH;
    } else if (token_buffer[0] == '(') {
        return SYM_PAREN_OPEN;
    } else if (token_buffer[0] == ')') {
        return SYM_PAREN_CLOSE;
    } else if (token_buffer[0] == '[') {
        return SYM_BRACKET_OPEN;
    } else if (token_buffer[0] == ']') {
        return SYM_BRACKET_CLOSE;
    } else if (token_buffer[0] == '{') {
        return SYM_BRACE_OPEN;
    } else if (token_buffer[0] == '}') {
        return SYM_BRACE_CLOSE;
    } else if (token_buffer[0] == '=') {
        return SYM_EQUAL;
    } else if (token_buffer[0] == '+') {
        return SYM_PLUS;
    } else if (token_buffer[0] == '-') {
        return SYM_DASH;
    } else if (token_buffer[0] == '/') {
        return SYM_FSLASH;
    } else if (token_buffer[0] == '*') {
        return SYM_STAR;
    } else if (token_buffer[0] == '%') {
        return SYM_PERCENT;
    } else if (token_buffer[0] == '!') {
        return SYM_EXCLAIM;
    } else if (token_buffer[0] == '<') {
        return SYM_LT;
    } else if (token_buffer[0] == '>') {
        return SYM_GT;
    } else if (token_buffer[0] == '&') {
        return SYM_AMPERSAND;
    } else if (token_buffer[0] == '|') {
        return SYM_PIPE;
    } else if (token_buffer[0] == '^') {
        return SYM_CARET;
    } else if (token_buffer[0] == '\'') {
        return SYM_SQUOTE;
    } else if (token_buffer[0] == '"') {
        return SYM_DQUOTE;
    } else if (!strncmp(token_buffer, "opt", MAX_IDENTIFIER_LENGTH)) {
        return KEYWORD_OPT;
    } else if (!strncmp(token_buffer, "void", MAX_IDENTIFIER_LENGTH)) {
        return KEYWORD_VOID;
    } else if (!strncmp(token_buffer, "char", MAX_IDENTIFIER_LENGTH)) {
        return KEYWORD_CHAR;
    } else if (!strncmp(token_buffer, "string", MAX_IDENTIFIER_LENGTH)) {
        return KEYWORD_STRING;
    } else if (!strncmp(token_buffer, "u8", MAX_IDENTIFIER_LENGTH)) {
        return KEYWORD_U8;
    } else if (!strncmp(token_buffer, "u16", MAX_IDENTIFIER_LENGTH)) {
        return KEYWORD_U16;
    } else if (!strncmp(token_buffer, "u32", MAX_IDENTIFIER_LENGTH)) {
        return KEYWORD_U32;
    } else if (!strncmp(token_buffer, "u64", MAX_IDENTIFIER_LENGTH)) {
        return KEYWORD_U64;
    } else if (!strncmp(token_buffer, "i8", MAX_IDENTIFIER_LENGTH)) {
        return KEYWORD_I8;
    } else if (!strncmp(token_buffer, "i16", MAX_IDENTIFIER_LENGTH)) {
        return KEYWORD_I16;
    } else if (!strncmp(token_buffer, "i32", MAX_IDENTIFIER_LENGTH)) {
        return KEYWORD_I32;
    } else if (!strncmp(token_buffer, "i64", MAX_IDENTIFIER_LENGTH)) {
        return KEYWORD_I64;
    } else if (!strncmp(token_buffer, "f32", MAX_IDENTIFIER_LENGTH)) {
        return KEYWORD_F32;
    } else if (!strncmp(token_buffer, "f64", MAX_IDENTIFIER_LENGTH)) {
        return KEYWORD_F64;
    } else if (!strncmp(token_buffer, "bool", MAX_IDENTIFIER_LENGTH)) {
        return KEYWORD_BOOL;
    } else if (!strncmp(token_buffer, "break", MAX_IDENTIFIER_LENGTH)) {
        return KEYWORD_BREAK;
    } else if (!strncmp(token_buffer, "case", MAX_IDENTIFIER_LENGTH)) {
        return KEYWORD_CASE;
    } else if (!strncmp(token_buffer, "mut", MAX_IDENTIFIER_LENGTH)) {
        return KEYWORD_MUT;
    } else if (!strncmp(token_buffer, "continue", MAX_IDENTIFIER_LENGTH)) {
        return KEYWORD_CONTINUE;
    } else if (!strncmp(token_buffer, "default", MAX_IDENTIFIER_LENGTH)) {
        return KEYWORD_DEFAULT;
    } else if (!strncmp(token_buffer, "else", MAX_IDENTIFIER_LENGTH)) {
        return KEYWORD_ELSE;
    } else if (!strncmp(token_buffer, "enum", MAX_IDENTIFIER_LENGTH)) {
        return KEYWORD_ENUM;
    } else if (!strncmp(token_buffer, "for", MAX_IDENTIFIER_LENGTH)) {
        return KEYWORD_FOR;
    } else if (!strncmp(token_buffer, "if", MAX_IDENTIFIER_LENGTH)) {
        return KEYWORD_IF;
    } else if (!strncmp(token_buffer, "return", MAX_IDENTIFIER_LENGTH)) {
        return KEYWORD_RETURN;
    } else if (!strncmp(token_buffer, "sizeof", MAX_IDENTIFIER_LENGTH)) {
        return KEYWORD_SIZEOF;
    } else if (!strncmp(token_buffer, "static", MAX_IDENTIFIER_LENGTH)) {
        return KEYWORD_STATIC;
    } else if (!strncmp(token_buffer, "struct", MAX_IDENTIFIER_LENGTH)) {
        return KEYWORD_STRUCT;
    } else if (!strncmp(token_buffer, "switch", MAX_IDENTIFIER_LENGTH)) {
        return KEYWORD_SWITCH;
    } else if (!strncmp(token_buffer, "def", MAX_IDENTIFIER_LENGTH)) {
        return KEYWORD_DEF;
    } else if (!strncmp(token_buffer, "while", MAX_IDENTIFIER_LENGTH)) {
        return KEYWORD_WHILE;
    } else if (!strncmp(token_buffer, "overload", MAX_IDENTIFIER_LENGTH)) {
        return KEYWORD_OVERLOAD;
    } else if (!strncmp(token_buffer, "asm", MAX_IDENTIFIER_LENGTH)) {
        return KEYWORD_ASM;
    } else if (!strncmp(token_buffer, "as", MAX_IDENTIFIER_LENGTH)) {
        return KEYWORD_AS;
    } else {
        return IDENTIFIER;
    }
}

bool str_is_identifier(const str* const s) {
    if (s == NULL || s->data == NULL) { return NULL; }

    for (size_t index = 0; index < str_len(s); index++) {
        const char c = s->data[index];
        if (!(isalnum(c) || c == '_')) {
            return false;
        }
    }

    return true;
}
