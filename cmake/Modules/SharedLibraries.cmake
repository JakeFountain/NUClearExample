# Copyright (C) 2013-2016 Trent Houliston <trent@houliston.me>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
# Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Find our globally shared libraries:
FIND_PACKAGE(fmt REQUIRED)
FIND_PACKAGE(YAML-CPP REQUIRED)
FIND_PACKAGE(Eigen3 REQUIRED)

# Set include directories and libraries:
INCLUDE_DIRECTORIES(SYSTEM ${fmt_INCLUDE_DIRS})
INCLUDE_DIRECTORIES(SYSTEM ${YAML-CPP_INCLUDE_DIRS})

SET(NUCLEAR_ADDITIONAL_SHARED_LIBRARIES
    ${fmt_LIBRARIES}
    ${YAML-CPP_LIBRARIES}
    CACHE STRING "" FORCE
)

IF(UNIX AND NOT APPLE)
    SET(NUCLEAR_ADDITIONAL_SHARED_LIBRARIES
        ${NUCLEAR_ADDITIONAL_SHARED_LIBRARIES}
        -pthread
        -ldl
        -lbacktrace
        CACHE STRING "" FORCE
    )
ENDIF()
