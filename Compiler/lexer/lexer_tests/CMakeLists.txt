add_executable(test_lexer_lib
    main.c
    test_lexer.c
    test_symlist.c
)

target_link_libraries(test_lexer_lib
    lexer_lib
    unity_lib
)

add_test(NAME "Lexer Tests" COMMAND test_lexer_lib)