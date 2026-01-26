add_library(parser_lib STATIC parser.c)
target_link_libraries(parser_lib lexer_lib str_lib)
target_include_directories(parser_lib PUBLIC ${CMAKE_CURRENT_LIST_DIR})

add_subdirectory(tests)