add_library(debug_lib STATIC
    debug.c
)

target_include_directories(debug_lib PUBLIC
    ${CMAKE_CURRENT_LIST_DIR}
)