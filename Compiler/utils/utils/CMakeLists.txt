add_library(utils_lib STATIC
    debug.c
    arena.c
    list.c
    str.c
    map.c
    bloom_filter.c
    hash.c
)

message("CTEST_FULL_OUTPUT")

target_include_directories(utils_lib PUBLIC
    ${CMAKE_CURRENT_LIST_DIR}
)