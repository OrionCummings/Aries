add_executable(test_lexer_lib
    test_lexer.c
)

target_link_libraries(test_lexer_lib
    lexer_lib
    unity_lib
    utils_lib
)

add_test(NAME "Lexer Tests" COMMAND test_lexer_lib)