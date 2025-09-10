add_executable(test_arena_lib
    test_arena.c
)

target_link_libraries(test_arena_lib
    unity_lib
    utils_lib
)

add_test(NAME "Arena Tests" COMMAND test_arena_lib)