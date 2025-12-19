#include "list.h"

/// @brief Creates a new list.
/// @param list The variable in which to place the new list.
/// @param callbacks The set of callbacks to use in this new list.
/// @return Returns true if this function was successful and false otherwise.
bool list_new(list_t** list, list_callbacks_t* callbacks) {

    // Allocate space for the list structure. Return early
    // if this doesn't succeed!
    *list = calloc(1, sizeof(**list));
    if (!*list) { return false; }

    // Allocate space for the list elements. Return early
    // if this doesn't succeed!
    (*list)->elements = calloc(LIST_DEFAULT_CAPACITY, sizeof(*(*list)->elements));
    if (!(*list)->elements) { return false; }

    // Set the list attributes to their default values.
    (*list)->capacity = LIST_DEFAULT_CAPACITY;
    (*list)->size = 0;

    // If the given callbacks are not NULL, then use them
    // to initialize the list.
    if (callbacks != NULL) {
        (*list)->callbacks.equal = callbacks->equal;
        (*list)->callbacks.copy = callbacks->copy;
        (*list)->callbacks.free = callbacks->free;
    }
    A_INFO("0x%p", (*list)->elements);
    return true;
}

/// @brief Deallocates the given list.
/// @param list The list to deallocate.
void list_free(list_t* list) {

    // If the given list is already null, then do nothing.
    if (list == NULL) {
        return;
    }

    // If the elements exist and there is a defined free function,
    // free each element with that free function.
    if (list->elements != NULL || list->callbacks.free != NULL) {
        for (size_t index = 0; index < list->size; ++index) {
            list->callbacks.free(list->elements[index]);
        }
    }

    // Free the elements and the list itself.
    free(list->elements);
    free(list);

    // Set list to null just to make sure ;)
    list = NULL;
}

/// @brief Gives the length of the given list.
/// @param list The list.
/// @param len The length of the list.
/// @return Returns true if this function was successful and false otherwise.
bool list_len(const list_t* list, size_t* len) {
    if (list == NULL) {
        *len = 0;
        return false;
    }

    if (len == NULL) {
        return false;
    }

    return list_len(list, len);
}

/// @brief Appends the given value to the given list. The size of the list
/// may be increased by this function.
/// @param list The list to which value is appended.
/// @param value The values to be added to the list.
/// @return Returns true if this function was successful and false otherwise.
bool list_append(list_t* list, void* value) {

    // If the given list or value are invalid,
    // then do nothing.
    if (list == NULL || value == NULL) {
        return false;
    }

    // Use the list insertion function to reuse code!
    return list_insert(list, value, list->size);
}

bool list_insert(list_t* list, void* value, size_t index) {

    // If the given list or value are invalid,
    // then do nothing.
    if (list == NULL || value == NULL) {
        return false;
    }

    // If the index to be added is greater than or equal to the current
    // size of the list, then we must allocate more space. Assign the
    // return value of realloc() to a temporary variable in case it
    // fails! Only after checking that it did not fail should we
    // actually assign it to the list.
    if (list->capacity >= index) {
        list->capacity *= LIST_DEFAULT_GROWTH_FACTOR;
        void* elements = realloc(list->elements,
            sizeof(*list->elements) * list->capacity);

        // Check if the reallocate fails; if so, return early.
        if (elements == NULL) {
            return false;
        }

        // Update the list with the reallocated memory.
        list->elements = elements;

        // If the index is within the range of the existing list, then
        // just add it to the requested index. Note that this does nothing
        // to handle overwritting existing values!
    } else {
        void* dest = list->elements + (index + 1); // The next available spot
        const void* src = list->elements + index; // The last item
        size_t length = (list->size - index) * sizeof(*list->elements);
        memmove(dest, src, length);
    }

    list->elements[index] = value;
    list->size++;

    return false;
}

bool list_remove(list_t*, size_t index) {

    return false;
}

bool list_index(const list_t*, const void*, size_t*) {

    return false;
}

void* list_get(const list_t* size_t) {

    return 0;
}

bool list_to_string(const list_t* list, char* buffer, list_var_t var) {
    return false;
}

void list_print(const list_t* list, list_var_t var) {

    printf("0x%p\n", (void*)list);
    printf("0x%p\n", (void*)list->elements);

    if (list == NULL || list->elements == NULL) {
        return;
    }
    
    float percent = (float)list->size / (float)list->capacity;
    printf("(%lu / %lu = %2.2f)", list->size, list->capacity, percent);

    for (size_t index = 0; index < list->size; ++index) {

        switch (var) {
            case (UCHAR): { printf("%c, ", *(unsigned char*)(list->elements[index])); break; }
            case (U8): { printf("%"PRIu8", ", *(uint8_t*)(list->elements[index])); break; }
            case (U16): { printf("%"PRIu16", ", *(uint16_t*)(list->elements[index])); break; }
            case (U32): { printf("%"PRIu32", ", *(uint32_t*)(list->elements[index])); break; }
            case (U64): { printf("%"PRIu64", ", *(uint64_t*)(list->elements[index])); break; }
            case (I8): { printf("%"PRIi8", ", *(int8_t*)(list->elements[index])); break; }
            case (I16): { printf("%"PRIi16", ", *(int16_t*)(list->elements[index])); break; }
            case (I32): { printf("%"PRIi32", ", *(int32_t*)(list->elements[index])); break; }
            case (I64): { printf("%"PRIi64", ", *(int64_t*)(list->elements[index])); break; }
            case (F32): { printf("%f, ", *(float*)(list->elements[index])); break; }
            case (F64): { printf("%lf, ", *(double*)(list->elements[index])); break; }
            default: {
                A_WARNING("Unknown list_var_t '%d'", var);
                break;
            }
        }
    }
    printf("\n");
}
