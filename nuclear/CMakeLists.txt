# We use additional modules for the NUClear roles system
SET(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_CURRENT_SOURCE_DIR}/cmake/Modules/")

# We need NUClear
FIND_PACKAGE(NUClear REQUIRED)
INCLUDE_DIRECTORIES(SYSTEM ${NUClear_INCLUDE_DIR})

# Set to off to ignore building tests
OPTION(BUILD_TESTS "Builds all of the tests for each module." OFF)

# Set to on to build as shared libraries
OPTION(NUCLEAR_SHARED_BUILD "Build each module as a separate shared library." ON)

# Our banner file for placing at the top of the roles
SET(NUCLEAR_ROLE_BANNER_FILE "${CMAKE_CURRENT_SOURCE_DIR}/roles/banner.png" CACHE PATH "The path the banner to print at the start of each role execution")

# Our location of our nuclear roles directory
SET(NUCLEAR_ROLES_DIR "${CMAKE_CURRENT_SOURCE_DIR}" CACHE PATH "The path to the nuclear roles system directory")

SET(NUCLEAR_ADDITIONAL_SHARED_LIBRARIES "" CACHE STRING "Additional libraries used when linking roles, extensions, and utilities")

SET(NUCLEAR_TEST_LIBRARIES "" CACHE STRING "Additional libraries used when linking module tests")

# Our variables that are used to locate the shared, module, and message folders
# They are given relative to the current project directory
SET(NUCLEAR_MODULE_DIR    "module"           CACHE PATH "The path to the module directory for NUClear")
SET(NUCLEAR_MESSAGE_DIR   "shared/message"   CACHE PATH "The path to the message directory for NUClear")
SET(NUCLEAR_UTILITY_DIR   "shared/utility"   CACHE PATH "The path to the utility dir for NUClear")
SET(NUCLEAR_EXTENSION_DIR "shared/extension" CACHE PATH "The path to the extension dir for NUClear")

# You generally shouldn't have to change these
MARK_AS_ADVANCED(NUCLEAR_ROLE_BANNER_FILE
                 NUCLEAR_MODULE_DIR
                 NUCLEAR_MESSAGE_DIR
                 NUCLEAR_UTILITY_DIR
                 NUCLEAR_EXTENSION_DIR)

# Make our shared directory to output files too
FILE(MAKE_DIRECTORY ${PROJECT_BINARY_DIR}/shared)

# Settings for the compiler to make NUClear work
INCLUDE(NUClearCompilerSettings)

# Add the subdirectory for our messages
ADD_SUBDIRECTORY("message")

# Add the subdirectory for our utilities
# Is after messages as it can use messages
ADD_SUBDIRECTORY("utility")

# Add the subdirectory for our extensions
ADD_SUBDIRECTORY("extension")

# Add the subdirectory for our roles
ADD_SUBDIRECTORY("roles")

# Add the subdirectory for module
# This must be after roles as roles determines which modules to build
ADD_SUBDIRECTORY("module")

