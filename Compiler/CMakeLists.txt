cmake_minimum_required(VERSION 4.0)
project(AriesCompiler VERSION 0.0.2 LANGUAGES C)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(CMAKE_C_STANDARD 23)
set(CMAKE_C_EXTENSIONS OFF)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_C_FLAGS_DEBUG "-g -DDEBUG")

add_compile_definitions(false=0)
add_compile_definitions(true=1)

add_subdirectory(src)
add_subdirectory(lexer)
add_subdirectory(parser)
add_subdirectory(external)

# if(TARGET_GROUP STREQUAL TEST)
#     message("Test build enabled...")
#     set(CTEST_OUTPUT_ON_FAILURE TRUE)
#     include(CTest)
#     add_subdirectory(lexer/lexer_tests)
# endif()
