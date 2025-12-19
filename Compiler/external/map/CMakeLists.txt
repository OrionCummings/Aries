add_library(map_lib STATIC
    map.c
)

target_link_libraries(map_lib PUBLIC
    debug_lib
    arena_lib
    hash_lib
)

target_include_directories(map_lib PUBLIC
    ${CMAKE_CURRENT_LIST_DIR}
)