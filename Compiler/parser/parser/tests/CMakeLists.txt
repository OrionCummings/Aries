add_executable(test_parser_lib
    test_parser.c
)
target_link_libraries(test_parser_lib unity_lib debug_lib parser_lib)
add_test(NAME "Parser Tests" COMMAND test_parser_lib)