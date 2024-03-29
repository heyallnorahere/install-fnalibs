cmake_minimum_required(VERSION 3.10)
set(FNALIBS_TARGET_DIRECTORY "The directory to copy binaries into" CACHE PATH ".")
set(FNALIBS SDL2 FAudio FNA3D)
message(STATUS "FNA libraries: ${FNALIBS}")
foreach(LIB ${FNALIBS})
    message(STATUS "Adding library: ${LIB}")
    add_subdirectory(${LIB})
    if(${LIB} STREQUAL "SDL2")
        set(SDL2_INCLUDE_DIRS "${CMAKE_CURRENT_SOURCE_DIR}/SDL2/include")
        set(SDL2_LIBRARIES SDL2::SDL2)
    endif()
endforeach()
set(PLATFORM_MACOSX ${UNIX} AND NOT ${APPLE})
if(WIN32 OR PLATFORM_MACOSX)
    message(STATUS "Adding copy target")
    foreach(LIB ${FNALIBS})
        list(APPEND OUTPUT_FILES $<TARGET_FILE:${LIB}>)
    endforeach()
    add_custom_target(COPY_BINARIES ALL
        COMMAND ${CMAKE_COMMAND} -E make_directory ${FNALIBS_TARGET_DIRECTORY}
        COMMAND ${CMAKE_COMMAND} -E copy_if_different ${OUTPUT_FILES} ${FNALIBS_TARGET_DIRECTORY}
        DEPENDS ${FNALIBS})
endif()