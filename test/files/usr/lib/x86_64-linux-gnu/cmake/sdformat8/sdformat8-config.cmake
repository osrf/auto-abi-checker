# We explicitly set the desired cmake version to ensure that the policy settings
# of users or of toolchains do not result in the wrong behavior for our modules.
# Note that the call to find_package(~) will PUSH a new policy stack before
# taking on these version settings, and then that stack will POP after the
# find_package(~) has exited, so this will not affect the cmake policy settings
# of a caller.
cmake_minimum_required(VERSION 3.10.2 FATAL_ERROR)

if(SDFormat_CONFIG_INCLUDED)
  return()
endif()
set(SDFormat_CONFIG_INCLUDED TRUE)


####### Expanded from @PACKAGE_INIT@ by configure_package_config_file() #######
####### Any changes to this file will be overwritten by the next CMake run ####
####### The input file was sdf_config.cmake.in                            ########

get_filename_component(PACKAGE_PREFIX_DIR "${CMAKE_CURRENT_LIST_DIR}/../../../../" ABSOLUTE)

# Use original install prefix when loaded through a "/usr move"
# cross-prefix symbolic link such as /lib -> /usr/lib.
get_filename_component(_realCurr "${CMAKE_CURRENT_LIST_DIR}" REALPATH)
get_filename_component(_realOrig "/usr/lib/x86_64-linux-gnu/cmake/sdformat8/" REALPATH)
if(_realCurr STREQUAL _realOrig)
  set(PACKAGE_PREFIX_DIR "/usr")
endif()
unset(_realOrig)
unset(_realCurr)

macro(set_and_check _var _file)
  set(${_var} "${_file}")
  if(NOT EXISTS "${_file}")
    message(FATAL_ERROR "File or directory ${_file} referenced by variable ${_var} does not exist !")
  endif()
endmacro()

####################################################################################

if(NOT TARGET sdformat8::sdformat8)
  include("${CMAKE_CURRENT_LIST_DIR}/sdformat8-targets.cmake")
endif()

list(APPEND SDFormat_INCLUDE_DIRS "/usr/include/sdformat-8.3")

list(APPEND SDFormat_CFLAGS "-I/usr/include/sdformat-8.3")
if (NOT WIN32)
  list(APPEND SDFormat_CXX_FLAGS "${SDFormat_CFLAGS} -std=c++17")
endif()

list(APPEND SDFormat_LIBRARY_DIRS "/usr/lib/x86_64-linux-gnu")

set(SDFormat_LIBRARIES sdformat8::sdformat8)

# These variables are used by ignition-cmake to automatically configure the
# pkgconfig files for ignition projects.
set(sdformat8_PKGCONFIG_ENTRY "sdformat8")
set(sdformat8_PKGCONFIG_TYPE PKGCONFIG_REQUIRES)

find_package(ignition-math6)
list(APPEND SDFormat_INCLUDE_DIRS ${IGNITION-MATH_INCLUDE_DIRS})
list(APPEND SDFormat_LIBRARY_DIRS ${IGNITION-MATH_LIBRARY_DIRS})

list(APPEND SDFormat_LDFLAGS "-L/usr/lib/x86_64-linux-gnu")
