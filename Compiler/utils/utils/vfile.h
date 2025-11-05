#ifndef __VFILE_H
#define __VFILE_H

#include <stdio.h>
#include "str.h"

/// NOTE: I don't think this is actually useful at the moment as the str struct is basically the same thing!

/// @brief A Virtual File. Used to abstract the notion of a file because the input of the compiler is ultimately just a string.
typedef struct {
    FILE* file;
    str* contents;
} vfile;

/// @brief Creates a new vfile instance from the given str.
/// @param s 
/// @return 
vfile* vfile_new(str* s);

void _vfile_free(vfile* vf);
#define vfile_free(vf) do{ \
    _vfile_free(vf);       \
    vf = NULL;             \
} while(0)                 \

#endif