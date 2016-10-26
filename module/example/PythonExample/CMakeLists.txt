FIND_PACKAGE(PythonInterp 3 REQUIRED)
FIND_PACKAGE(pybind11 REQUIRED)
FIND_PACKAGE(PythonLibsNew 3 REQUIRED)

GET_FILENAME_COMPONENT(MODULE_NAME ${CMAKE_CURRENT_SOURCE_DIR} NAME)

# Calculate the Output Directory
FILE(MAKE_DIRECTORY "${PROJECT_BINARY_DIR}/python/nuclear")

# Create symlinks to the files
ADD_CUSTOM_COMMAND(
    OUTPUT "${PROJECT_BINARY_DIR}/python/nuclear/nuclear.py"
    COMMAND ${CMAKE_COMMAND} -E create_symlink "${PROJECT_SOURCE_DIR}/nuclear/module/python/nuclear.py" "${PROJECT_BINARY_DIR}/python/nuclear/nuclear.py"
    DEPENDS "${PROJECT_SOURCE_DIR}/nuclear/module/python/nuclear.py"
    COMMENT "Creating a symbolic link for nuclear.py"
)

MESSAGE("${CMAKE_CURRENT_SOURCE_DIR}/python/nuclear.py")
MESSAGE("${PROJECT_BINARY_DIR}/python/nuclear/nuclear.py")


FILE(MAKE_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/src/")

ADD_CUSTOM_COMMAND(
    OUTPUT "${CMAKE_CURRENT_BINARY_DIR}/src/${MODULE_NAME}.h"
           "${CMAKE_CURRENT_BINARY_DIR}/src/${MODULE_NAME}.cpp"
    COMMAND ${CMAKE_COMMAND}
    ARGS -E env
        PYTHONPATH="${NUCLEAR_ROLES_DIR}/module/python/"
        NUCLEAR_MODULE_DIR="${PROJECT_SOURCE_DIR}/${NUCLEAR_MODULE_DIR}"
    ${PYTHON_EXECUTABLE} "${CMAKE_CURRENT_SOURCE_DIR}/src/${MODULE_NAME}.py"
    WORKING_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/src"
    DEPENDS "src/${MODULE_NAME}.py"
            "${NUCLEAR_ROLES_DIR}/module/python/nuclear.py"
    COMMENT "Generating bindings for python module ${MODULE_NAME}")

# Now copy all our python files across to the python directory of output
FILE(GLOB_RECURSE python_files "${CMAKE_CURRENT_SOURCE_DIR}/src/**.py")

UNSET(python_code)

# Process the data files
FOREACH(python_file ${python_files})

    # Calculate the output Directory
    FILE(RELATIVE_PATH output_file "${PROJECT_SOURCE_DIR}/${NUCLEAR_MODULE_DIR}" ${python_file})
    SET(output_file "${PROJECT_BINARY_DIR}/python/${output_file}")

    # Add the file we will generate to our output
    LIST(APPEND python_code ${output_file})

    # Create the required folder
    GET_FILENAME_COMPONENT(output_folder ${output_file} DIRECTORY)
    FILE(MAKE_DIRECTORY ${output_folder})

    MESSAGE("${PROJECT_BINARY_DIR}/python/nuclear/nuclear.py")

    # Create symlinks to the files
    ADD_CUSTOM_COMMAND(
        OUTPUT ${output_file}
        COMMAND ${CMAKE_COMMAND} -E create_symlink ${python_file} ${output_file}
        DEPENDS ${python_file}
                "${PROJECT_BINARY_DIR}/python/nuclear/nuclear.py"
        COMMENT "Creating symbolic link for file ${python_file}"
    )

ENDFOREACH(python_file)

# Build our NUClear module
NUCLEAR_MODULE(SOURCES "${CMAKE_CURRENT_BINARY_DIR}/src/${MODULE_NAME}.h"
                       "${CMAKE_CURRENT_BINARY_DIR}/src/${MODULE_NAME}.cpp"
                       ${python_code})
