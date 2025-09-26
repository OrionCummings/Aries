#include "lexer.h"

const char* const TOKEN_NAMES[] = {
    [INVALID] = "INVALID",
    [NONE] = "NONE",
    [IDENTIFIER] = "IDENTIFIER",
    [SYM_EOF] = "SYM_EOF",
    [SYM_SEMICOLON] = "SYM_SEMICOLON",
    [SYM_COLON] = "SYM_COLON",
    [SYM_COMMA] = "SYM_COMMA",
    [SYM_QUESTION] = "SYM_QUESTION",
    [SYM_FSLASH] = "SYM_FSLASH",
    [SYM_PAREN_OPEN] = "SYM_PAREN_OPEN",
    [SYM_PAREN_CLOSE] = "SYM_PAREN_CLOSE",
    [SYM_BRACKET_OPEN] = "SYM_BRACKET_OPEN",
    [SYM_BRACKET_CLOSE] = "SYM_BRACKET_CLOSE",
    [SYM_BRACE_OPEN] = "SYM_BRACE_OPEN",
    [SYM_BRACE_CLOSE] = "SYM_BRACE_CLOSE",
    [SYM_EQUAL] = "SYM_EQUAL",
    [SYM_PLUS] = "SYM_PLUS",
    [SYM_DASH] = "SYM_DASH",
    [SYM_SLASH] = "SYM_SLASH",
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

    bool complete = false;
    while (!complete) {
        Symbol* next_symbol = lex_next(lexer);

        A_INFO("Parsed symbol '%s' (%d)", next_symbol->s, TOKEN_NAMES[next_symbol->t]);

        switch (next_symbol->t) {
            case(SYM_EOF):
            case(NONE): // Intentional fall-through
                complete = true;

            default:
                if (!lex_append(lexer, *next_symbol)) {
                    A_WARNING("Failed to append symbol '%s' (%d)", next_symbol->s, TOKEN_NAMES[next_symbol->t]);
                    complete = true;
                }
        }

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

Symbol* lex_next(Lexer* lexer) {

    if (lexer == NULL) { A_WARNING("Passed null parameter 'lexer'"); return NULL; }

    // NOTE: This limits the size of identifiers to 255 characters; I don't care!
    static char token_buffer[MAX_IDENTIFIER_LENGTH] = { 0 };
    size_t token_buffer_index = 0;

    char c;
    bool boundary = false;
    while (!boundary) {
        boundary = lex_boundary(lexer);
        c = (char)fgetc(lexer->file);

        if (token_buffer_index == MAX_IDENTIFIER_LENGTH) {
            A_ERROR("Encountered token longer than 256 characters!");
            return INVALID;
        }
        token_buffer[token_buffer_index++] = c;
    }

    Token token = lex_buffer_to_token(token_buffer);
    Symbol* sym = sym_new(token, token_buffer);

    A_INFO("token_buffer = '%s'", token_buffer);
    A_INFO("token = '%s' (%d)", TOKEN_NAMES[token], token);
    A_INFO("sym = '%s' ('%s')", sym->s, TOKEN_NAMES[sym->t]);

    memset(token_buffer, 0, MAX_IDENTIFIER_LENGTH);
    return sym;
}

bool lex_boundary(Lexer* lexer) {
    static bool run = false;

    long position = ftell(lexer->file);
    char first_char = (char)fgetc(lexer->file);
    char second_char = lex_peek(lexer);
    fseek(lexer->file, position, SEEK_SET);

    if (!run) { 
        run = true;
        return !is_identifier_char(first_char);
    }

    return is_identifier_char(first_char) ^ is_identifier_char(second_char);
}

char lex_peek(Lexer* lexer) {
    long position = ftell(lexer->file);
    if (position == -1) { A_WARNING("ftell(lexer->file) failed!"); return '\0'; }
    char c = (char)fgetc(lexer->file);
    fseek(lexer->file, position, SEEK_SET);
    return c;
}

bool lex_append(Lexer* lexer, Symbol sym) {
    return true;
}

bool is_identifier_char(char c) {
    return (isalnum(c) || c == '_');
}

Symbol* sym_new(Token t, char* s) {
    void* maybe_sym = calloc(1, sizeof(Symbol));
    if (maybe_sym == NULL) {
        A_WARNING("failed to allocate new symbol");
        return NULL;
    }
    return (Symbol*)maybe_sym;
}

void sym_free_(Symbol* s) {
    if (s != NULL) {
        free(s->s);
    }
    free(s);
}

Token lex_buffer_to_token(char token_buffer[MAX_IDENTIFIER_LENGTH]) {

    // TODO: Come back here and appreciate how awful this is. Go on. Do it.
    // Refactor it, coward.
    if (token_buffer[0] == EOF) {
        return SYM_EOF;
    } else if (token_buffer[0] == ' ') {
        return WHITESPACE;
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

