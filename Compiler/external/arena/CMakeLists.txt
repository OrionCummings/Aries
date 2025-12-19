add_library(arena_lib STATIC arena.c)
target_link_libraries(arena_lib PUBLIC debug_lib)
target_include_directories(arena_lib PUBLIC ${CMAKE_CURRENT_LIST_DIR})

add_executable(test_arena_lib test_arena.c)
target_link_libraries(test_arena_lib unity_lib debug_lib arena_lib)
add_test(NAME "Arena Tests" COMMAND arena_lib)
