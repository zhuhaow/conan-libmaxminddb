cmake_minimum_required(VERSION 2.8.12)
project(PackageTest C)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

if (WIN32)
  SET(LIBS ${CONAN_LIBS} ws2_32)
else
  SET(LIBS ${CONAN_LIBS})
endif

add_executable(example example.c)
target_link_libraries(example ${LIBS})

# CTest is a testing tool that can be used to test your project.
enable_testing()
add_test(NAME example
         WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/bin
         COMMAND example)
