#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "sdformat8::sdformat8" for configuration "RelWithDebInfo"
set_property(TARGET sdformat8::sdformat8 APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(sdformat8::sdformat8 PROPERTIES
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/x86_64-linux-gnu/libsdformat8.so.8.3.0"
  IMPORTED_SONAME_RELWITHDEBINFO "libsdformat8.so.8"
  )

list(APPEND _IMPORT_CHECK_TARGETS sdformat8::sdformat8 )
list(APPEND _IMPORT_CHECK_FILES_FOR_sdformat8::sdformat8 "${_IMPORT_PREFIX}/lib/x86_64-linux-gnu/libsdformat8.so.8.3.0" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
