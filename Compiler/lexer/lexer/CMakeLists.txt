add_library(lexer_lib STATIC
    lexer.c
    token.c
    symbol.c
    sym_list.c
)

target_link_libraries(lexer_lib
    str_lib
)

target_include_directories(lexer_lib PUBLIC
    ${CMAKE_CURRENT_LIST_DIR}
)