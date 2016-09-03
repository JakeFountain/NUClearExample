#!/usr/bin/env python3
from nuclear import Reactor, on, Trigger

class P(object):
    pass

@Reactor
class PythonExample(object):

    @on(Trigger(P))
    def an_example_function(self, p):
        print(p)

# This is what the final c++ should look like
"""

// SOMEWHERE IN SOME OTHER GLOBAL PYTHON ENABLER FILE WHICH RUNS ONCE FOR WHOLE SYSTEM
// BEFORE IT STARTS RUNNING PYTHON CODE
PyImport_AppendInittab("message", &PyInit_message);
Py_Initialize();
PyEval_InitThreads();

namespace A {
namespace B {

    class {PythonReactorName} {

        PyInterpreterState* interpreter = nullptr;
        PyObject* self = nullptr;
        thread_local PyThreadState* thread_state = nullptr;

        // Constructor
        {PythonReactorName}() {

            // This sets the threadstate/interpreter combination for
            // the thread that creates this interperter
            thread_state = Py_NewInterpreter();

            // Store a pointer to our newly created interpreter
            interpreter = thread_state->interp;

            // TODO somewhere I need to set the self variable to an instance of the reactor class

            // TODO open the .py file and let it run!
            // If we setup everything properly here it should call the appropriate c++ functions and make things happen
        }

        // Generated for the python function an_example_function
        auto bind_an_example_function(pybind11::function pyfn) {

            return on<DSL...>(runtimeargs).then([this, fn] (args...) {

                // Create our thread state for this thread if it doesn't exist
                if (!thread_state) {
                    thread_state = PyThreadState_New(interpreter);
                }

                // Load our thread state and obtain the GIL
                PyEval_RestoreThread(thread_state);

                // Run the python function
                fn(self, args...);

                // Release the GIL and set our thread back to nullptr
                PyEval_SaveThread()
            });
        }
    }

}
}
"""
