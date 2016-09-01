#ifndef MODULE_EXAMPLE_PYTHONEXAMPLE_H
#define MODULE_EXAMPLE_PYTHONEXAMPLE_H

#include <nuclear>

namespace module {
namespace example {

    class PythonExample : public NUClear::Reactor {

    public:
        /// @brief Called by the powerplant to build and setup the PythonExample reactor.
        explicit PythonExample(std::unique_ptr<NUClear::Environment> environment);
    };

}
}

#endif  // MODULE_EXAMPLE_PYTHONEXAMPLE_H
