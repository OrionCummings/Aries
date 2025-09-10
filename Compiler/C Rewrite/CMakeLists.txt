cmake_minimum_required(VERSION 4.0)
project(AriesCompiler VERSION 0.0.2 LANGUAGES C)

set(CMAKE_C_STANDARD 23)
set(CMAKE_C_EXTENSIONS OFF)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

add_subdirectory(src)
add_subdirectory(utils)

if(TARGET_GROUP STREQUAL test)
  include(CTest)
  add_subdirectory(external)
  add_subdirectory(utils/utils_tests)
endif()