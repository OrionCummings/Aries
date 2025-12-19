add_library(str_lib STATIC str.c)
target_link_libraries(str_lib PUBLIC arena_lib)
target_include_directories(str_lib PUBLIC ${CMAKE_CURRENT_LIST_DIR})

add_executable(test_str_lib test_str.c)
target_link_libraries(test_str_lib unity_lib debug_lib str_lib)
add_test(NAME "String Tests" COMMAND test_str_lib)