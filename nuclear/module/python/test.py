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
// BEFORE IT STARTS RUNNING PYTHON CODE (doesn't have to be generated here)
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

            // Create a module object that holds our binding functions
            pybind11::module module("nuclear", "Binding functions for the current nuclear_reactor");

            // TODO also here create on Trigger etc (dsl keywords) and attach them to NUClear
            // They should basically be noop types now (except for on and reactor which should call the appropriate binding functions)

            // Create a function that binds the self object
            m.def("bind_self", [this] (pybind11::object obj) {
                self = obj;
            })

            // Create a function that can be called to bind this function
            m.def("bind_{an_example_function}", [this] (pybind11::function fn, runtimeargs?) {

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
            });
            ....etc

            // Take our created module and add it to this subinterpreters imports
            PyImport_AddModule("nuclear_reactor");
            PyObject* sys_modules = PyImport_GetModuleDict();
            PyDict_SetItemString(sys_modules, "nuclear_reactor", module.ptr());

            // TODO open the .py file and let it run!
            // If we setup everything properly here it should call the appropriate c++ functions and make things happen
        }
    }

}
}

"""
