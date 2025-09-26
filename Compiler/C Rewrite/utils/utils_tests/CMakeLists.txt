add_executable(test_arena_lib
    test_arena.c
)

add_executable(test_str_lib
    test_str.c
)

target_link_libraries(test_arena_lib
    unity_lib
    utils_lib
)

target_link_libraries(test_str_lib
    unity_lib
    utils_lib
)

add_test(NAME "Arena Tests" COMMAND test_arena_lib)
add_test(NAME "String Tests" COMMAND test_str_lib)