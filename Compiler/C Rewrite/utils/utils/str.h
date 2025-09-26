#ifndef __STR_H
#define __STR_H

#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

/// @brief An immutable string. Usually allocated on the heap, but this is not always true, especially with string views.
typedef struct {
    bool heap;
    size_t length;
    char* data;
} str;

/// @brief A list of strings
typedef struct {
    size_t size;
    size_t capacity;
    str* strings;
} list_str;

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
/// @param s1 A string instance
/// @param s2 A string instance
/// @return A new string instance of the form s1s2.
str* str_concat(str* s1, str* s2);

/// @brief Compares two strings s1 and s2 character-wise. This does not account for differences in length (which shouldn't happen?), capacity, or heap status; this function only checks character content. If strict equality is required, use `str_ident()`
/// @param s1 A string instance
/// @param s2 A string instance
/// @return Returns true if the string data in both strings are equal and false otherwise.
bool str_cmp(const str* const s1, const str* const s2);

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
/// @param s1 The string in which to search for `s2`.
/// @param s2 The string to search for in `s1`.
/// @return Returns true if `s2` occurs in `s1`.
int str_sub(const str* const s1, const str* const s2);

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

/// @brief Returns a view of `s`. Does not free `s`! The returned string has the `heap` field set to false! The return value of this function should never be passed as an argument to `str_free`
/// @param s The underlying string.
/// @param start The starting index of the view (inclusive).
/// @param end The ending index of the view (exclusive).
/// @return A new string instance referencing the characters from `start` to `end`, inclusive.
str* str_view(const str* const s, size_t start, size_t end);

/// @brief Splits `s` at each instance of `c` and returns a list of string views ... Does not free `s`.
/// @param s The string to split.
/// @param c The delimiting character.
/// @return A list of string views.
list_str* str_split(const str* const s, char c);

/// @brief Prints the given string.
/// @param s The string to print.
void str_print(const str* const s);

#endif