import inspect
import re
import os
from textwrap import dedent

def indent(str, len=4):
    return '\n'.join([(' ' * len) + l for l in str.splitlines()])

class DSLWord(object):
    pass

# Single type keywords

class SingleTypeDSLWord(DSLWord):

    def __init__(self, t):
        self._name = self.__class__.__name__
        self._t = t

    def template_args(self):
        return "{}<::{}::{}>".format(self._name, self._t.__module__.replace('.', '::'), self._t.__name__.replace('.', '::'))

class Trigger(SingleTypeDSLWord): pass
class With(SingleTypeDSLWord): pass
class Sync(SingleTypeDSLWord): pass

# No arg Keywords

class NoArgsDSLWord(DSLWord):
    def __init__(self):
        self._name = self.__class__.__name__

    def template_args(self):
        return self._name

class Always(NoArgsDSLWord): pass
class MainThread(NoArgsDSLWord): pass
class Single(NoArgsDSLWord): pass
class Startup(NoArgsDSLWord): pass
class Shutdown(NoArgsDSLWord): pass

# DSL modifiers

class Last(DSLWord):
    def __init__(self, dsl, count):
        self._name = self.__class__.__name__
        self._dsl = dsl
        self._count = count

    def template_args(self):
        return "{}<{}, {}>".format(self._name, self._count, self._dsl.template_args())

    def runtime_args(self):
        return self._dsl.runtime_args()

class Optional(DSLWord):
    def __init__(self, dsl):
        self._name = self.__class__.__name__
        self._dsl = dsl

    def template_args(self):
        return "{}<{}>".format(self._name, self._dsl.template_args())

    def runtime_args(self):
        return self._dsl.runtime_args()

# Weird types

class Buffer(DSLWord):
    def __init__(self, k):
        self._name = self.__class__.__name__
        self._k = k

    def template_args(self):
        return "{}<{}>".format(self._name, self._k)

class Every(DSLWord):
    pass

class Priority(object):
    class REALTIME(DSLWord):
        def template_arg(self):
            return "Priority::REALTIME"

    class HIGH(DSLWord):
        def template_arg(self):
            return "Priority::HIGH"

    class NORMAL(DSLWord):
        def template_arg(self):
            return "Priority::NORMAL"

    class LOW(DSLWord):
        def template_arg(self):
            return "Priority::LOW"

    class IDLE(DSLWord):
        def template_arg(self):
            return "Priority::IDLE"


# Type that holds a DSL function

class DSLCallback(DSLWord):

    def __init__(self, func, *dsl):
        self.func = func
        self._t_args = ", ".join(w.template_args() for w in dsl if hasattr(w, 'template_args') and w.template_args())
        self._r_args = ", ".join(w.runtime_args()  for w in dsl if hasattr(w, 'runtime_args')  and w.runtime_args())

    def template_args(self):
        return self._t_args

    def runtime_args(self):
        return self._r_args

    def function(self):
        return self.func

# Decorator for creating instance variables/setting up reactor
def Reactor(reactor):

    # Get the filename of the reactor
    reactor_name = os.path.abspath(inspect.stack()[1].filename)

    # Get the module base directory
    module_dir = os.getenv('NUCLEAR_MODULE_DIR', '')
    #NOTE: this is lazy, since it assumes the reactor path is the same as the module path
    module_depth = len(module_dir.strip(os.sep).split(os.sep))

    # Extract path info
    reactor_path = reactor_name.split(os.sep)
    module_path = reactor_path[module_depth:reactor_path.index('src')]
    reactor_name = module_path[-1]

    # Get our reactions
    reactions = inspect.getmembers(reactor, predicate=lambda x: isinstance(x, DSLCallback))

    binder_impl = dedent("""\
        // Binding function for the dsl on<{dsl}>
        m.def("bind_{func_name}", [this] (pybind11::function fn) {{

            return on<{dsl}>().then([this, fn] (args...) {{

                // Create our thread state for this thread if it doesn't exist
                if (!thread_state) {{
                    thread_state = PyThreadState_New(interpreter);
                }}

                // Load our thread state and obtain the GIL
                PyEval_RestoreThread(thread_state);

                // Run the python function
                fn(self, args...);

                // Release the GIL and set our thread back to nullptr
                PyEval_SaveThread();
            }});
        }});""")

    binders = set()

    # Loop through our reactions and add handler functions for them
    for reaction in reactions:
        func_name = re.sub(r'(?:\W|^(?=\d))+', '_', reaction[1].template_args())

        binders.add(binder_impl.format(func_name=func_name,
            dsl=reaction[1].template_args()))

    class_name = str(reactor.__name__)
    open_namespace = "namespace " + str('::'.join(module_path)) + " {"
    close_namespace = "}  // " + str('::'.join(module_path))
    macro_guard = "{}_H".format(class_name.upper())
    header_file = "{}.h".format(class_name)

    header_template = dedent("""\
        #ifndef {macro_guard}
        #define {macro_guard}

        #include <nuclear>

        {open_namespace}

            class {class_name} : public NUClear::Reactor {{
            public:
                // Constructor
                explicit {class_name}(std::unique_ptr<NUClear::Environment> environment);

            private:
                // The subinterpreter for this module
                PyInterpreterState* interpreter = nullptr;

                // The self object for this module
                PyObject* self = nullptr;

                // The thread state for this thread/interpreter combination
                thread_local PyThreadState* thread_state = nullptr;
            }};
        {close_namespace}

        #endif  // {macro_guard}""")

    with open(os.getcwd() + os.sep + reactor_name + '.h', 'w') as f:
        f.write(header_template.format(class_name=class_name,
            macro_guard=macro_guard,
            open_namespace=open_namespace,
            close_namespace=close_namespace))

    cpp_template = dedent("""\
        #include "{header_file}"

        #include <pybind11/pybind11.h>
        #include <pybind11/functional.h>

        {open_namespace}

            {class_name}::{class_name}(std::unique_ptr<NUClear::Environment> environment)
            : Reactor(std::move(environment)) {{
                // If python hasn't been used in another module yet
                if (!Py_IsInitialized()) {{
                    // Add our message to our initilsation
                    PyImport_AppendInittab("message", &PyInit_message);

                    // Initialise without signal handlers
                    Py_InitializeEx(0);

                    // Initialise using threads in python
                    PyEval_InitThreads();
                }}

                // This sets the threadstate/interpreter combination for
                // the thread that creates this interperter
                thread_state = Py_NewInterpreter();

                // Store a pointer to our newly created interpreter
                interpreter = thread_state->interp;

                // Create a module object that holds our binding functions
                pybind11::module module("nuclear", "Binding functions for the current nuclear reactor");

                // Create a function that binds the self object for passing into callbacks
                m.def("bind_self", [this] (PyObject* obj) {{
                    self = obj;
                }});

        {binders}

                // Take our created module and add it to this subinterpreters imports
                PyImport_AddModule("nuclear_reactor");
                PyObject* sys_modules = PyImport_GetModuleDict();
                PyDict_SetItemString(sys_modules, "nuclear_reactor", module.ptr());

                // Now open up our main python file and run it to bind all the functions
            }}

        {close_namespace}""")

    with open(os.getcwd() + os.sep + reactor_name + '.cpp', 'w') as f:
        f.write(cpp_template.format(header_file=header_file,
            class_name=class_name,
            binders=indent('\n\n'.join(binders), 8),
            open_namespace=open_namespace,
            close_namespace=close_namespace))

    return reactor

# Our on function that creates the binding
def on(*args):

    def decorator(func):

        return DSLCallback(func, *args)

    return decorator

# TYPES THAT I DON'T KNOW IF I WANT

# IO? probably has no analouge in python
# TCP
# UDP

# Network
