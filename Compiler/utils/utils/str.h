#ifndef __STR_H
#define __STR_H

#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <ctype.h>
#include <errno.h>
#include <stdint.h>

// TODO: Handle capitalized variants!
#define PREFIX_BIN ("0b")
#define PREFIX_OCT ("0o")
#define PREFIX_HEX ("0x")

#define U8_SUFFIX  ("u8")
#define U16_SUFFIX ("u16")
#define U32_SUFFIX ("u32")
#define U64_SUFFIX ("u64")

#define I8_SUFFIX  ("i8")
#define I16_SUFFIX ("i16")
#define I32_SUFFIX ("i32")
#define I64_SUFFIX ("i64")

#define F32_SUFFIX ("f32")
#define F64_SUFFIX ("f64")

#define BOOL_SUFFIX ("b") // TODO: is this something i want?

/// @brief An immutable string. Usually allocated on the heap.
typedef struct {
    bool heap;
    size_t length;
    char* data;
} str;

/// @brief 
typedef size_t index_t;

/// @brief Allocates a new string instance based on the given cstring.
/// @param s The target cstring.
/// @return A heap-allocated str* instance.
str* str_new(const char* s);

/// @brief Frees the given string and sets it to zero.
/// @param s The string instance to free.
#define str_free(s) do{ \
    _str_free(s);       \
    s = NULL;           \
} while(0)              \

/// @brief Private function for freeing string instances. Do not use this function directly. Use str_free() instead.
void _str_free(str* s);

/// @brief Concatenates two string instances.
/// @param s1 A string.
/// @param s2 A string.
/// @return A new string instance of the form s1s2.
str* str_concat(str* s1, str* s2);

/// @brief Compares two strings s1 and s2 character-wise. This does not account for differences in length (which shouldn't happen?), capacity, or heap status; this function only checks character content. If strict equality is required, use `str_ident()`.
/// @param s1 A string.
/// @param s2 A string.
/// @return Returns true if the string data in both strings are equal and false otherwise.
bool str_cmp(const str* const s1, const str* const s2);

/// @brief Compares a string `s` and a c-string `cs` for equality.
/// @param s A string.
/// @param cs A c-string.
/// @return Returns true if the string data in `s` is equal to the c-string `cs` and false otherwise.
bool str_cmp_raw(const str* const s, const char* const cs);

/// @brief Compares two strings s1 and s2 character-wise and accounts for differences in length, capacity, and allocation status. If mear character equality is desired, use `str_cmp()` instead.
/// @param s1 A string instance
/// @param s2 A string instance
/// @return Returns true if both strings are identical and false otherwise.
bool str_ident(const str* const s1, const str* const s2);

/// @brief Find the index of `c` in `s`.
/// @param s The string in which to search for `c`.
/// @param c The character to find.
/// @return The first index of `c` in `s`. If `c` is not in `s`, returns -1.
int str_find(const str* const s, const char c);

/// @brief Returns
/// @param s The string in which to search for `sub`.
/// @param sub The 'sub' string to search for in `s`.
/// @return Returns the index at which `sub` occurs in `s`. Returns -1 if `sub` does not occur in `s`.
int str_sub(const str* const s, const str* const sub);

/// @brief Returns the length of `s`.
/// @param s The target string.
/// @return The length of the given string.
size_t str_len(const str* const s);

/// @brief Returns the character at `index` in `s`.
/// @param s The string in which to search.
/// @param index The index to check.
/// @return The character at the index in the string. Returns the null character if the index exceeds the size of the given string.
char str_at(const str* const s, size_t index);

/// @brief Appends `c` to the end of `s`. This function will always allocate a new string instance to add the new character; therefore, this function cannot append characters to stack-allocated strings.
/// @param s The string to which `c` is to be appended.
/// @param c The character to append to `s`. This character cannot be null as that would break compatability with traditional cstrings AND invalidate an assumption with the return value of `str_at` (on failure, return null char).
/// @return Returns a new string instance if the character is appended; otherwise, return NULL.
str* str_append(const str* const s, const char c);

/// @brief Returns a view of `s`. The returned string has the `heap` field set to false! The return value of this function should never be passed as an argument to `str_free`. The behavior of this function is undefined if the underlying string is freed.
/// @param s The underlying string.
/// @param start The starting index of the view (inclusive).
/// @param end The ending index of the view (inclusive).
/// @return A new string instance referencing the characters from `start` to `end`, inclusive.
str* str_view(const str* const s, size_t start, size_t end);

/// @brief Returns a new copy of `s`.
/// @param s The string to copy.
/// @param start The index at which to start the copy.
/// @param end The index at which to end the copy.
/// @return A new string instance.
str* str_copy(const str* const s, size_t start, size_t end);

/// @brief NOT IMPLEMENTED; MAY BE USEFUL.
str** str_split(const str* const s, char c);

/// @brief Returns a copy of the underlying character array.
/// @param s The string from which to copy.
/// @return A heap-allocated pointer to a copy of the string.
char* str_raw(const str* const s);

/// @brief Returns a string instance containing the contents of `file`.
/// @param file The file to convert to a string.
/// @return A string instance containing the contents of `file`.
str* str_from_file(FILE* const file);

/// @brief Returns a string instance containing the contents of `file`.
/// @param filename The filename of the file to convert to a string.
/// @return A string instance containing the contents of the file `filename`.
str* str_from_filename(const char* filename);

/// @brief Removes `c` from both the left and right ends of `s`. This function will modify the underlying string but will not reallocate any memory. This function will only remove one instance of `c` from either end. If `c` is not on the ends of `s`, then this function does nothing.
/// 
/// Example:
/// 
/// s = "test"; str_strip(s, 't') = "es"
/// 
/// @param s The string from which `c` is to be removed.
/// @param c The character that is to be removed from `s`.
/// @return `s` without `c` on the left and right ends.
str* str_strip(str* s, const char c);

/// @brief Returns true if `s` begins with `prefix`.
/// @param s A string.
/// @param prefix A c-string.
/// @return Returns true if `s` begins with `prefix`, otherwise returns false.
bool str_has_prefix(const str* const s, const char* prefix);

/// @brief Returns true if `s` ends with `suffix`.
/// @param s A string.
/// @param suffix A c-string.
/// @return Returns true if `s` ends with `suffix`, otherwise returns false.
bool str_has_suffix(const str* const s, const char* suffix);

/// @brief Prints the given string.
/// @param s The string to print.
void str_print(const str* const s);

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