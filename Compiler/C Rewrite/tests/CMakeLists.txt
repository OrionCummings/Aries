add_executable(test_lib
    test_example.c
)

target_link_libraries(test_lib
    unity_lib
    utils_lib
)

add_test(NAME "Test 1" COMMAND test_lib)