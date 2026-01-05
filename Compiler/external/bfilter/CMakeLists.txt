add_library(bfilter_lib STATIC
    bfilter.c
)

target_link_libraries(bfilter_lib PUBLIC
    debug_lib
    hash_lib
    arena_lib
)

target_include_directories(bfilter_lib PUBLIC
    ${CMAKE_CURRENT_LIST_DIR}
)

add_subdirectory(tests)