#ifndef POINT_H
#define POINT_H

#define TEST_DIRECTIVE 672
#ifdef TEST_DIRECTIVE
// This comment should only appear if TEST_DIRECTIVE is recognized correctly!
#endif

typedef struct point {
    int x;
    int y;
} point;

#endif