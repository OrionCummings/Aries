cmake_minimum_required(VERSION 4.0)
project(AriesEmulator VERSION 0.0.1 LANGUAGES C)

set(CMAKE_C_STANDARD 23)
set(CMAKE_C_EXTENSIONS OFF)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_C_FLAGS_DEBUG "-g -DDEBUG")

add_compile_definitions(false=0)
add_compile_definitions(true=1)

add_subdirectory(src)
add_subdirectory(external)

