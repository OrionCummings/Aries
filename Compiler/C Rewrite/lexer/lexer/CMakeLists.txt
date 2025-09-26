add_library(lexer_lib STATIC
    lexer.c
)

target_link_libraries(lexer_lib
    utils_lib
)

target_include_directories(lexer_lib PUBLIC
    ${CMAKE_CURRENT_LIST_DIR}
)