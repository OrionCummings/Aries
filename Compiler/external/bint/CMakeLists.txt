add_library(bint_lib STATIC
    bint.c
)

target_include_directories(bint_lib PUBLIC
    ${CMAKE_CURRENT_LIST_DIR}
)

target_link_libraries(bint_lib
    debug_lib
    str_lib
)

add_subdirectory(tests)